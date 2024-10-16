#
# Function app definition
#

locals {
  onboarding_app_settings = {
    FUNCTIONS_WORKER_RUNTIME              = "node"
    FUNCTIONS_WORKER_PROCESS_COUNT        = "4"
    NODE_ENV                              = "production"
    FETCH_KEEPALIVE_ENABLED               = "true"
    FETCH_KEEPALIVE_SOCKET_ACTIVE_TTL     = "110000"
    FETCH_KEEPALIVE_MAX_SOCKETS           = "40"
    FETCH_KEEPALIVE_MAX_FREE_SOCKETS      = "10"
    FETCH_KEEPALIVE_FREE_SOCKET_TIMEOUT   = "30000"
    FETCH_KEEPALIVE_TIMEOUT               = "60000"
    CONTRACTS_TOPIC_CONSUMER_GROUP        = "$Default"
    CONTRACTS_CONSUMER_CONNECTION_STRING  = "${data.azurerm_key_vault_secret.sc_contracts_conn_string.value}"
    CONTRACTS_TOPIC_NAME                  = "sc-contracts"
    SLACK_WEBHOOK_LOG                     = "${data.azurerm_key_vault_secret.slack_webhook_log.value}"
    SLACK_WEBHOOK_ONBOARDING_IO           = "${data.azurerm_key_vault_secret.slack_webhook_onboarding_io.value}"
    SLACK_WEBHOOK_ONBOARDING_IO_PREMIUM   = "${data.azurerm_key_vault_secret.slack_webhook_onboarding_io_premium.value}"
    SLACK_WEBHOOK_ONBOARDING_PN           = "${data.azurerm_key_vault_secret.slack_webhook_onboarding_pn.value}"
    SLACK_WEBHOOK_ONBOARDING_INTEROP      = "${data.azurerm_key_vault_secret.slack_webhook_onboarding_interop.value}"
    SLACK_WEBHOOK_ONBOARDING_PAGOPA       = "${data.azurerm_key_vault_secret.slack_webhook_onboarding_pagopa.value}"
    OCP_APIM_SUBSCRIPTION_KEY             = "${data.azurerm_key_vault_secret.ocp_apim_subscription_key.value}"
    ENDPOINT_GET_INSTITUTION_FROM_TAXCODE = "https://api.selfcare.pagopa.it/external/v2/institutions/?taxCode="
  }
}

module "onboarding_snet" {
  source                                    = "git::https://github.com/pagopa/terraform-azurerm-v3.git//subnet?ref=v8.26.2"
  name                                      = format("%s-onboarding-snet-01", local.project)
  address_prefixes                          = var.cidr_onboarding_fn
  resource_group_name                       = data.azurerm_virtual_network.vnet.resource_group_name
  virtual_network_name                      = data.azurerm_virtual_network.vnet.name
  private_endpoint_network_policies_enabled = false

  service_endpoints = [
    "Microsoft.Web",
    "Microsoft.AzureCosmosDB",
    "Microsoft.Storage",
  ]

  delegation = {
    name = "default"
    service_delegation = {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

module "onboarding_fn" {
  source = "git::https://github.com/pagopa/terraform-azurerm-v3.git//function_app?ref=v8.26.2"

  resource_group_name = azurerm_resource_group.rg_common.name
  name                = format("%s-onboarding-fn-01", local.project)
  location            = var.location
  domain              = local.application_basename
  health_check_path   = "/api/v1/info"

  node_version    = "18"
  runtime_version = "~4"

  always_on                                = "true"
  application_insights_instrumentation_key = "foo" //TODO add ai reference

  app_service_plan_info = {
    kind                         = var.function_onboarding_config.kind
    sku_tier                     = var.function_onboarding_config.sku_tier
    sku_size                     = var.function_onboarding_config.sku_size
    maximum_elastic_worker_count = 0
    worker_count                 = 1
    zone_balancing_enabled       = false
  }

  app_settings = merge(
    local.onboarding_app_settings,
    {},
  )

  sticky_app_setting_names = []

  storage_account_name         = replace(format("%sonboardingfnst01", local.project), "-", "")
  storage_account_durable_name = replace(format("%sonboardingfnst01", local.project), "-", "")

  storage_account_info = {
    account_kind                      = "StorageV2"
    account_tier                      = "Standard"
    account_replication_type          = "ZRS"
    access_tier                       = "Hot"
    advanced_threat_protection_enable = false
    use_legacy_defender_version       = false
    public_network_access_enabled     = true
  }

  internal_storage = {
    "enable"                     = true,
    "private_endpoint_subnet_id" = data.azurerm_subnet.pendpoints_snet.id,
    "private_dns_zone_blob_ids"  = [data.azurerm_private_dns_zone.privatelink_blob_core.id],
    "private_dns_zone_queue_ids" = [data.azurerm_private_dns_zone.privatelink_queue_core.id],
    "private_dns_zone_table_ids" = [data.azurerm_private_dns_zone.privatelink_table_core.id],
    "queues"                     = [],
    "containers"                 = [],
    "blobs_retention_days"       = 0,
  }
  subnet_id = module.onboarding_snet.id

  system_identity_enabled = true

  tags = var.tags
}

resource "azurerm_monitor_autoscale_setting" "function_onboarding" {
  name                = format("%s-autoscale-01", module.onboarding_fn.name)
  resource_group_name = azurerm_resource_group.rg_common.name
  location            = var.location
  target_resource_id  = module.onboarding_fn.app_service_plan_id

  profile {
    name = "default"

    capacity {
      default = 1
      minimum = 1
      maximum = 30
    }

    rule {
      metric_trigger {
        metric_name              = "Requests"
        metric_resource_id       = module.onboarding_fn.id
        metric_namespace         = "microsoft.web/sites"
        time_grain               = "PT1M"
        statistic                = "Average"
        time_window              = "PT1M"
        time_aggregation         = "Average"
        operator                 = "GreaterThan"
        threshold                = 3500
        divide_by_instance_count = false
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "2"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name              = "CpuPercentage"
        metric_resource_id       = module.onboarding_fn.app_service_plan_id
        metric_namespace         = "microsoft.web/serverfarms"
        time_grain               = "PT1M"
        statistic                = "Average"
        time_window              = "PT5M"
        time_aggregation         = "Average"
        operator                 = "GreaterThan"
        threshold                = 60
        divide_by_instance_count = false
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "2"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name              = "Requests"
        metric_resource_id       = module.onboarding_fn.id
        metric_namespace         = "microsoft.web/sites"
        time_grain               = "PT1M"
        statistic                = "Average"
        time_window              = "PT15M"
        time_aggregation         = "Average"
        operator                 = "LessThan"
        threshold                = 2500
        divide_by_instance_count = false
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT10M"
      }
    }

    rule {
      metric_trigger {
        metric_name              = "CpuPercentage"
        metric_resource_id       = module.onboarding_fn.app_service_plan_id
        metric_namespace         = "microsoft.web/serverfarms"
        time_grain               = "PT1M"
        statistic                = "Average"
        time_window              = "PT5M"
        time_aggregation         = "Average"
        operator                 = "LessThan"
        threshold                = 30
        divide_by_instance_count = false
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT20M"
      }
    }
  }
}
