terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.81.0"
    }
  }
}
resource "aws_lambda_function" "lambda_function" {
  function_name = var.lambda_name
  role          = var.role_arn
  runtime       = "python3.11"
  handler       = "main.lambda_handler"

  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  environment {
    variables = {
      SESSION_SECRET_NAME = "ool/bluesky/token",
      BLUE_SKY_CREDENTIALS_SECRET_NAME = "ool/bluesky/credentials",
    }
  }

  timeout = 10
  memory_size = 128
}

resource "aws_lambda_event_source_mapping" "mapping" {
  function_name = aws_lambda_function.lambda_function.arn
  event_source_arn = var.queue_processing_trends
  batch_size = 1
}
