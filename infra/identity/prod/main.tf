terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.106.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfinfprodio"
    container_name       = "terraform-state"
    key                  = "sm-infra.identity.prod.westeurope.tfstate"
  }
}

provider "azurerm" {
  features {}
}

module "federated_identities" {
  source = "github.com/pagopa/dx//infra/modules/azure_federated_identity_with_github?ref=main"

  prefix       = local.prefix
  env_short    = local.env_short
  env          = "prod"
  domain       = local.domain
  repositories = [local.repo_name]
  tags         = local.tags

  continuos_delivery = {
    enable = true
    roles = {
      subscription = ["Contributor"]
      resource_groups = {
        terraform-state-rg = [
          "Storage Blob Data Contributor"
        ],
        # TODO fix data rg
        # ts-p-itn-data-rg-01 = [
        #   "Role Based Access Control Administrator"
        # ]
      }
    }
  }
}

module "app_federated_identities" {
  source = "github.com/pagopa/dx//infra/modules/azure_federated_identity_with_github?ref=main"

  prefix       = local.prefix
  env_short    = local.env_short
  env          = "app-prod"
  domain       = "${local.domain}-app"
  repositories = [local.repo_name]
  tags         = local.tags
}

module "federated_identity_ci_roles" {
  source = "github.com/pagopa/dx//infra/modules/azure_role_assignments?ref=main"

  principal_id = module.federated_identities.federated_ci_identity.id

  key_vault = [
    {
      name                = "${local.prefix}-${local.domain}-${local.env_short}-${local.location_short}-kv-01"
      resource_group_name = "${local.prefix}-${local.domain}-${local.env_short}-${local.location_short}-common-rg"
      roles = {
        secrets = "reader"
      }
    },
    {
      name                = "${local.prefix}-${local.env_short}-kv"
      resource_group_name = "${local.prefix}-${local.env_short}-sec-rg"
      roles = {
        secrets = "reader"
      }
    }
  ]
}

module "federated_identity_cd_roles" {
  source = "github.com/pagopa/dx//infra/modules/azure_role_assignments?ref=main"

  principal_id = module.federated_identities.federated_cd_identity.id

  key_vault = [
    {
      name                = "${local.prefix}-${local.domain}-${local.env_short}-${local.location_short}-kv-01"
      resource_group_name = "${local.prefix}-${local.domain}-${local.env_short}-${local.location_short}-common-rg"
      roles = {
        secrets = "reader"
      }
    },
    {
      name                = "${local.prefix}-${local.env_short}-kv"
      resource_group_name = "${local.prefix}-${local.env_short}-sec-rg"
      roles = {
        secrets = "reader"
      }
    }
  ]
}