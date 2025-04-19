# Deploy Azure Sentinel Analytics Rules
# Uses the ARM template for deploying analytics rules

# Deploy the analytics rules using ARM template deployment
resource "azurerm_resource_group_template_deployment" "sentinel_analytics_rules" {
  name                = "${var.prefix}-analytics-rules"
  resource_group_name = azurerm_resource_group.rg.name
  deployment_mode     = "Incremental"
  parameters_content = jsonencode({
    "workspace" = {
      value = azurerm_log_analytics_workspace.law.name
    }
  })
  template_content = file("${path.module}/Azure_Sentinel_analytics_rules.json")

  depends_on = [
    azurerm_sentinel_log_analytics_workspace_onboarding.sentinel
  ]
}
