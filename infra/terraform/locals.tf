locals {
  name_prefix = lower(replace(var.project_name, " ", "-"))
  tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment
    },
    var.extra_tags
  )
}
