terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "<= 3.116.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "<= 2.33.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "<= 4.0.4"
    }
    local = {
      source  = "hashicorp/local"
      version = "<= 2.3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "<= 3.2.1"
    }
    random = {
      source  = "hashicorp/random"
      version = "<= 3.4.3"
    }
    azapi = {
      source  = "azure/azapi"
      version = "<= 1.9.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfinfprodio"
    container_name       = "terraform-state"
    key                  = "sm-infra.prod.tfstate"
  }
}

provider "azurerm" {
  features {}
}

provider "azapi" {
}

module "commons" {
  source = "../modules/commons"

  env_short = local.env_short

  cidr_onboarding_fn = ["10.20.7.0/27"]
  cidr_ask_bot_fn = ["10.20.4.64/27"]
  tags               = local.tags
}

module "grafana" {
  source = "../modules/grafana"

  env_short      = local.env_short
  prefix         = "io"
  location       = "westeurope"
  location_short = local.location_short["westeurope"]

  tags = local.tags
}
