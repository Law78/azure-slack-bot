# Service Management - GitHub federated Managed Identities

<!-- markdownlint-disable -->
<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | >= 3.106.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 3.110.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_app_federated_identities"></a> [app\_federated\_identities](#module\_app\_federated\_identities) | github.com/pagopa/dx//infra/modules/azure_federated_identity_with_github | main |
| <a name="module_federated_identities"></a> [federated\_identities](#module\_federated\_identities) | github.com/pagopa/dx//infra/modules/azure_federated_identity_with_github | main |
| <a name="module_federated_identity_cd_roles"></a> [federated\_identity\_cd\_roles](#module\_federated\_identity\_cd\_roles) | github.com/pagopa/dx//infra/modules/azure_role_assignments | main |
| <a name="module_federated_identity_ci_roles"></a> [federated\_identity\_ci\_roles](#module\_federated\_identity\_ci\_roles) | github.com/pagopa/dx//infra/modules/azure_role_assignments | main |

## Resources

| Name | Type |
|------|------|
| [azurerm_subscription.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/subscription) | data source |

## Inputs

No inputs.

## Outputs

No outputs.
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
