output "project_name" { value = var.project_name }

output "artifact_bucket" { value = aws_s3_bucket.artifacts.bucket }

output "base_url" {
  value = aws_apigatewayv2_stage.prod.invoke_url
}
