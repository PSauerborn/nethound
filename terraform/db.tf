
resource "aws_db_subnet_group" "main" {
  # add db subnet group for private subnet
  subnet_ids = [
    aws_subnet.public_subnet_alpha.id,
    aws_subnet.public_subnet_beta.id
  ]

  tags = {
    Name = "nethound-public-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 10

  # define postgres engine settings
  engine               = "postgres"
  engine_version       = "13.4"
  instance_class       = "db.t3.micro"

  # define instance settings
  identifier           = "${var.name}db${var.environment}"
  username             = var.postgres_username
  password             = var.postgres_password

  # define vpc and subnet settings
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [
    aws_security_group.postgres.id
  ]

  skip_final_snapshot  = true
  publicly_accessible  = true

  apply_immediately    = true
  multi_az             = false
}

# create security group for application loadbalancer
# which defines HTTPS and HTTP ports as valid
resource "aws_security_group" "postgres" {
  name   = "${var.name}-sg-db-${var.environment}-ext"
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol         = "tcp"
    from_port        = 5432
    to_port          = 5432
    cidr_blocks      = ["80.189.76.214/32"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 5432
    to_port          = 5432
    security_groups  = [aws_security_group.ecs_tasks.id]
  }


  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["80.189.76.214/32"]
    ipv6_cidr_blocks = ["::/0"]
  }
}