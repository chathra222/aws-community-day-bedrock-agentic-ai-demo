output "lambda_function_name" {
  value = aws_lambda_function.self_heal_lambda.function_name
}

output "bedrock_agent_id" {
  value = aws_bedrock_agent.playwright_agent.id
}