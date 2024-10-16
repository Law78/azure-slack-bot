data "azurerm_virtual_network" "vnet" {
  name                = "io-p-itn-common-vnet-01"
  resource_group_name = "io-p-itn-common-rg-01"
}

data "azurerm_subnet" "pendpoints_snet" {
  name                 = "io-p-itn-pep-snet-01"
  virtual_network_name = "io-p-itn-common-vnet-01"
  resource_group_name  = "io-p-itn-common-rg-01"
}

data "azurerm_private_dns_zone" "privatelink_blob_core" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = "io-p-rg-common"
}
data "azurerm_private_dns_zone" "privatelink_queue_core" {
  name                = "privatelink.queue.core.windows.net"
  resource_group_name = "io-p-rg-common"
}
data "azurerm_private_dns_zone" "privatelink_table_core" {
  name                = "privatelink.table.core.windows.net"
  resource_group_name = "io-p-rg-common"
}