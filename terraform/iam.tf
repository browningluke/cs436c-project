# Assume Role policy

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# IAM Role

resource "aws_iam_role" "lambda_iam" {
  name               = "${local.group_prefix}-lambda_iam"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json

  tags = merge({}, local.tags)
}

# == Allow Role to access S3 buckets ==

data "aws_iam_policy_document" "lambda_s3_policy" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]

    resources = [
      aws_s3_bucket.statement_ingestion.arn,
      "${aws_s3_bucket.statement_ingestion.arn}/*",
      aws_s3_bucket.customer_reports.arn,
      "${aws_s3_bucket.customer_reports.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "lambda_s3" {
  name        = "${local.group_prefix}-lambda_s3"
  path        = "/"
  description = "IAM policy for access to s3 from a lambda"
  policy      = data.aws_iam_policy_document.lambda_s3_policy.json

  tags = merge({}, local.tags)
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.lambda_iam.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

# == Allow Role (Lambda) to create logging events ==

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "${local.group_prefix}-lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json

  tags = merge({}, local.tags)
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_iam.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
