locals {
  prefix    = "io-sm"
  env_short = "p"

  location_short = { westeurope = "weu", italynorth = "itn", germanywestcentral = "gwc", northeurope = "neu" }

  tags = {
    CreatedBy      = "Terraform"
    Environment    = "Prod"
    Owner          = "SM"
    Source         = "https://github.com/pagopa/io-service-management"
    CostCenter     = "TS310 - PAGAMENTI & SERVIZI"
    ManagementTeam = "IO Service Management"
  }
}