locals {
  prefix    = "io"
  env_short = "p"

  location_short = "itn"
  location       = "italynorth"
  domain         = "sm"
  project        = "${local.prefix}-${local.env_short}-${local.domain}"

  repo_name = "io-service-management"

  identity_rg = "${local.prefix}-${local.env_short}-identity-rg"

  tags = {
    CreatedBy      = "Terraform"
    Environment    = "Prod"
    Owner          = "SM"
    Source         = "https://github.com/pagopa/io-service-management"
    CostCenter     = "TS310 - PAGAMENTI & SERVIZI"
    ManagementTeam = "IO Service Management"
  }
}
