locals {
  prefix         = "io"
  env_short      = "p"
  domain         = "sm"
  location_short = "itn"
  location       = "italynorth"
  project        = "${local.prefix}-${local.env_short}"

  tags = {
    CostCenter     = "TS310 - PAGAMENTI & SERVIZI"
    CreatedBy      = "Terraform"
    Environment    = "Prod"
    Owner          = "SM"
    ManagementTeam = "IO Service Management"
    Source         = "https://github.com/pagopa/io-service-management/infra/github-runner/prod"
  }
}
