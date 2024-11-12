resource "aws_s3_bucket" "statement_ingestion" {
  bucket = "${local.group_prefix}-statement-ingestion"

  tags = merge({
    Name = "Statement Ingestion"
  }, local.tags)
}

resource "aws_s3_bucket" "customer_reports" {
  bucket = "${local.group_prefix}-customer-reports"

  tags = merge({
    Name = "Customer Reports"
  }, local.tags)
}
