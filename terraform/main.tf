provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_iam_role" "lambda_role" {
  name = "playwright_self_heal_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
    }],
  })
}

resource "aws_iam_policy_attachment" "attach_basic_execution" {
  name       = "attach_basic_execution"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "self_heal_lambda" {
  function_name = "playwrightSelfHeal"
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_role.arn
  filename      = "lambda_function_payload.zip"
  timeout       = 300
  memory_size   = 512

  environment {
    variables = {
      GITHUB_TOKEN = var.github_token
      AGENT_ID     = var.agent_id
    }
  }
}

resource "aws_bedrock_agent" "playwright_agent" {
  agent_name = "PlaywrightSelfHealAgent"
  instructions = file("${path.module}/../agent/orchestration.yaml")
  foundation_model = "anthropic.claude-3-sonnet-2024-04-09-v1:0"
}

output "lambda_function_name" {
  value = aws_lambda_function.self_heal_lambda.function_name
}

output "agent_id" {
  value = aws_bedrock_agent.playwright_agent.id
}