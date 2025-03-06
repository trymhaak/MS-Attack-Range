# Microsoft Defender for Endpoint Connector
resource "azurerm_sentinel_data_connector_microsoft_defender_advanced_threat_protection" "defender" {
  name               = "defender-endpoint"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}

# Office 365 Connector
resource "azurerm_sentinel_data_connector_office_365" "o365" {
  name                       = "office-365"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  exchange_enabled          = true
  sharepoint_enabled       = true
  teams_enabled            = true
}

# Azure AD (Entra ID) Connector
resource "azurerm_sentinel_data_connector_azure_active_directory" "aad" {
  name                       = "entra-id"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}

# Data provider for current subscription
data "azurerm_subscription" "current" {}
