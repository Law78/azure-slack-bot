data "azurerm_key_vault" "key_vault" {
  name                = "${local.project}-kv"
  resource_group_name = "${local.project}-sec-rg"
}

data "azurerm_key_vault_secret" "smtp" {
  name         = "${local.project}-grafana-smtp-password"
  key_vault_id = data.azurerm_key_vault.key_vault.id
}