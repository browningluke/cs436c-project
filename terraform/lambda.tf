locals {
  function_name = "${local.group_prefix}-analysis-lambda"
}

data "archive_file" "lambda" {
  type        = "zip"
  source_file = "../app/lambda_function.py"
  output_path = "lambda_function_payload.zip"
}

# Log group for Lambda logs
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = 3

  tags = merge({}, local.tags)
}

resource "aws_lambda_function" "analysis_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = local.function_name
  role          = aws_iam_role.lambda_iam.arn
  handler       = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.10"

  logging_config {
    log_format = "JSON"
  }

  tags = merge({}, local.tags)

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_iam_role_policy_attachment.lambda_s3,
    aws_cloudwatch_log_group.lambda_logs,
  ]
}

# Allow S3 bucket to execute Lambda function
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.analysis_lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.statement_ingestion.arn
}

# Cause Lambda function execution when s3:ObjectCreated:* event seen on bucket
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.statement_ingestion.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.analysis_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    # filter_prefix       = "AWSLogs/"
    # filter_suffix       = ".log"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}
