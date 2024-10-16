#tfsec:ignore:azure-keyvault-specify-network-acl:exp:2022-05-01 # already ignored, maybe a bug in tfsec
module "key_vault" {
  source                     = "git::https://github.com/pagopa/terraform-azurerm-v3.git//key_vault?ref=v8.26.2"
  name                       = "${local.project}-kv-01"
  location                   = azurerm_resource_group.rg_common.location
  resource_group_name        = azurerm_resource_group.rg_common.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 15
  lock_enable                = false

  tags = var.tags
}

data "azurerm_key_vault_secret" "sc_contracts_conn_string" {
  name         = "sc-contracts-conn-string"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "slack_webhook_log" {
  name         = "slack-webhook-log"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "slack_webhook_onboarding_io" {
  name         = "slack-webhook-onboarding-io"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "slack_webhook_onboarding_pn" {
  name         = "slack-webhook-onboarding-pn"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "slack_webhook_onboarding_interop" {
  name         = "slack-webhook-onboarding-interop"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "ocp_apim_subscription_key" {
  name         = "ocp-apim-subscription-key"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "slack_webhook_onboarding_io_premium" {
  name         = "slack-webhook-onboarding-io-premium"
  key_vault_id = module.key_vault.id
}

data "azurerm_key_vault_secret" "slack_webhook_onboarding_pagopa" {
  name         = "slack-webhook-onboarding-pagopa"
  key_vault_id = module.key_vault.id
}
