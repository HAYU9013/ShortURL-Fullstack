resource "random_password" "docdb" {
  length  = 32
  special = false
}

resource "aws_docdb_subnet_group" "this" {
  name       = "${local.name_prefix}-${var.environment}-docdb"
  subnet_ids = aws_subnet.private[*].id

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-docdb-subnet-group"
  })
}

resource "aws_docdb_cluster" "this" {
  cluster_identifier              = "${local.name_prefix}-${var.environment}-docdb"
  engine                          = "docdb"
  master_username                 = "appuser"
  master_password                 = random_password.docdb.result
  backup_retention_period         = var.docdb_backup_retention_period
  preferred_backup_window         = "03:00-05:00"
  preferred_maintenance_window    = "sun:05:00-sun:06:00"
  db_subnet_group_name            = aws_docdb_subnet_group.this.name
  vpc_security_group_ids          = [aws_security_group.docdb.id]
  storage_encrypted               = true
  deletion_protection             = true
  apply_immediately               = false
  enabled_cloudwatch_logs_exports = ["audit", "profiler", "slowquery"]
  port                           = var.docdb_port
  copy_tags_to_snapshot           = true

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-docdb"
  })
}

resource "aws_docdb_cluster_instance" "this" {
  count              = var.docdb_instance_count
  identifier         = "${local.name_prefix}-${var.environment}-docdb-${count.index}"
  cluster_identifier = aws_docdb_cluster.this.id
  instance_class     = var.docdb_instance_class
  apply_immediately  = false

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-docdb-instance-${count.index}"
  })
}

resource "aws_secretsmanager_secret" "docdb" {
  name = "${local.name_prefix}/${var.environment}/docdb"

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-docdb-secret"
  })
}

resource "aws_secretsmanager_secret_version" "docdb" {
  secret_id     = aws_secretsmanager_secret.docdb.id
  secret_string = jsonencode({
    username = aws_docdb_cluster.this.master_username
    password = random_password.docdb.result
  })
}

resource "aws_secretsmanager_secret" "backend_env" {
  name = "${local.name_prefix}/${var.environment}/backend"

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-backend-secret"
  })
}

resource "aws_secretsmanager_secret_version" "backend_env" {
  secret_id     = aws_secretsmanager_secret.backend_env.id
  secret_string = jsonencode({
    MONGO_URL        = "mongodb://${aws_docdb_cluster.this.master_username}:${random_password.docdb.result}@${aws_docdb_cluster.this.endpoint}:${var.docdb_port}/${var.docdb_database}?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
    MONGO_TLS        = "true"
    MONGO_REPLICA_SET = "rs0"
    MONGO_READ_PREFERENCE = "secondaryPreferred"
    ALLOWED_ORIGINS  = join(",", length(var.allowed_origins) > 0 ? var.allowed_origins : ["https://${var.frontend_subdomain}"])
    LOG_LEVEL        = "info"
  })
}
