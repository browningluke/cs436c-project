resource "aws_ecr_repository" "ecr_repo" {
  name                 = "${local.group_prefix}-analysis"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge({}, local.tags)
}
