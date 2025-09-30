output "project_name" { value = var.project_name }

output "artifact_bucket" { value = "${var.project_name}-artifacts-${data.aws_caller_identity.me.account_id}" }

output "base_url" {
  value = aws_apigatewayv2_stage.prod.invoke_url
}
