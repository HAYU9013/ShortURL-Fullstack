resource "aws_security_group" "alb" {
  name        = "${local.name_prefix}-${var.environment}-alb-sg"
  description = "Allow inbound HTTP/HTTPS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-alb-sg"
  })
}

resource "aws_security_group" "ecs" {
  name        = "${local.name_prefix}-${var.environment}-ecs-sg"
  description = "Allow traffic from ALB and to DocumentDB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description                = "Allow traffic from ALB"
    from_port                  = 3000
    to_port                    = 3000
    protocol                   = "tcp"
    security_groups            = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-ecs-sg"
  })
}

resource "aws_security_group" "docdb" {
  name        = "${local.name_prefix}-${var.environment}-docdb-sg"
  description = "Allow DocumentDB access from ECS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "DocumentDB access"
    from_port       = var.docdb_port
    to_port         = var.docdb_port
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-${var.environment}-docdb-sg"
  })
}
