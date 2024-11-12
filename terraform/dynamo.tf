resource "aws_dynamodb_table" "statement_table" {
  name         = "${local.group_prefix}-statements"
  billing_mode = "PAY_PER_REQUEST"
  # read_capacity  = 20
  # write_capacity = 20
  hash_key  = "UserId"
  range_key = "YearMonth"

  attribute {
    name = "UserId"
    type = "S"
  }

  attribute {
    name = "YearMonth"
    type = "S"
  }

  # ttl {
  #   attribute_name = "TimeToExist"
  #   enabled        = true
  # }

  tags = merge({}, local.tags)
}

resource "aws_dynamodb_table" "user_table" {
  name         = "${local.group_prefix}-users"
  billing_mode = "PAY_PER_REQUEST"
  # read_capacity  = 20
  # write_capacity = 20
  hash_key = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }

  tags = merge({}, local.tags)
}
