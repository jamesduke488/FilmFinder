data "aws_caller_identity" "me" {}

resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.project_name}-artifacts-${data.aws_caller_identity.me.account_id}"
  force_destroy = true
}

resource "aws_lambda_function" "api" {
  function_name = "${var.project_name}-lambda"
  role          = aws_iam_role.lambda_exec.arn
  runtime       = "python3.12"
  handler       = "main.handler"

  s3_bucket = aws_s3_bucket.artifacts.id
  s3_key    = var.artifact_key

  timeout = 10
  environment {
    variables = {
      OMDB_API_KEY = data.aws_ssm_parameter.omdb.value
    }
  }
}