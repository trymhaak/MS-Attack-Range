# Microsoft Defender for Endpoint Connector
resource "azurerm_sentinel_data_connector_microsoft_defender_advanced_threat_protection" "defender" {
  count              = var.enable_premium_connectors ? 1 : 0
  name               = "defender-endpoint"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  depends_on = [azurerm_log_analytics_workspace.law, azurerm_sentinel_log_analytics_workspace_onboarding.sentinel]
}

# Office 365 Connector
resource "azurerm_sentinel_data_connector_office_365" "o365" {
  count                    = var.enable_premium_connectors ? 1 : 0
  name                       = "office-365"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  exchange_enabled          = true
  sharepoint_enabled       = true
  teams_enabled            = true
  depends_on = [azurerm_log_analytics_workspace.law, azurerm_sentinel_log_analytics_workspace_onboarding.sentinel]
}

# Azure AD (Entra ID) Connector
resource "azurerm_sentinel_data_connector_azure_active_directory" "aad" {
  count                    = var.enable_premium_connectors ? 1 : 0
  name                       = "entra-id"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  depends_on = [azurerm_log_analytics_workspace.law, azurerm_sentinel_log_analytics_workspace_onboarding.sentinel]
}

# XDR Connector
resource "azurerm_sentinel_data_connector_microsoft_threat_protection" "xdr" {
  count                    = var.enable_premium_connectors ? 1 : 0
  name                       = "MicrosoftDefenderXDRConnector"
 log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
 depends_on = [azurerm_log_analytics_workspace.law, azurerm_sentinel_log_analytics_workspace_onboarding.sentinel]
}

# Diagnostic settings to send Azure Activity Logs to Log Analytics
resource "azurerm_monitor_diagnostic_setting" "activity_logs" {
  name                           = "activity-logs-to-sentinel"
  target_resource_id             = "/subscriptions/${data.azurerm_subscription.current.subscription_id}"
  log_analytics_workspace_id     = azurerm_log_analytics_workspace.law.id

  enabled_log {
    category = "Administrative"
  }
  enabled_log {
    category = "Security"
  }
  enabled_log {
    category = "Policy"
  }
  enabled_log {
    category = "Alert"
  }
  enabled_log {
    category = "Recommendation"
  }
  enabled_log {
    category = "ServiceHealth"
  }
  enabled_log {
    category = "ResourceHealth"
  }
  enabled_log {
    category = "Autoscale"
  }
  depends_on = [azurerm_log_analytics_workspace.law, azurerm_sentinel_log_analytics_workspace_onboarding.sentinel]
}
# Data provider for current subscription
data "azurerm_subscription" "current" {}
