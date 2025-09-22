resource "aws_s3_bucket" "artifacts" {
  bucket = var.artifact_bucket
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