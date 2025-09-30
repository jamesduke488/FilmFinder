resource "aws_iam_role" "lambda_exec" {
  name               = "${var.project_name}-lambda-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
  force_detach_policies = true

  tags = {
    Project = "${var.project_name}"
    ManagedBy = "terraform"
  }
}

data "aws_iam_policy_document" "lambda_trust" {
  statement {
    effect = "Allow"
    
    principals { 
        type = "Service" 
        identifiers = ["lambda.amazonaws.com"] 
    }
    
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy_attachment" "basic_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Allow SSM read for OMDb key
resource "aws_iam_policy" "ssm_read" {
  name   = "${var.project_name}-ssm-read"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["ssm:GetParameter", "ssm:GetParameters"]
      Resource = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.me.account_id}:parameter/filmFinder/omdbApiKey"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_ssm_read" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.ssm_read.arn
}

