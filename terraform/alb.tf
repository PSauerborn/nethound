###########################
# Load balancer definitions
###########################

resource "aws_lb" "main" {
  name               = "${var.name}-alb-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]

  # add private and public subnets to loadbalancer
  subnets = [
    aws_subnet.public_subnet_alpha.id,
    aws_subnet.public_subnet_beta.id
  ]
  enable_deletion_protection = false

}

# create security group for application loadbalancer
# which defines HTTPS and HTTP ports as valid
resource "aws_security_group" "alb" {
  name   = "${var.name}-sg-alb-${var.environment}"
  vpc_id = aws_vpc.vpc.id

  ingress {
    protocol         = "tcp"
    from_port        = 80
    to_port          = 80
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 443
    to_port          = 443
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    protocol         = "tcp"
    from_port        = 50051
    to_port          = 50051
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# manage HTTPS traffic via target group
resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_lb.main.id
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = 443
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# manage HTTPS traffic via target group
resource "aws_alb_listener" "https" {
  load_balancer_arn = aws_lb.main.id
  port              = 443
  protocol          = "HTTPS"

  certificate_arn = var.certificate_arn

  default_action {
    target_group_arn = aws_alb_target_group.http.id
    type             = "forward"
  }
}

# define target group to receive HTTPS traffic.
# the target group can then be references by the
# ECS service to receive traffic from the loadbalancer
resource "aws_alb_target_group" "http" {
  name        = "${var.name}-tg-${var.environment}-http"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.vpc.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "120"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/health_check"
    unhealthy_threshold = "2"
  }
}

# manage HTTPS traffic via target group
resource "aws_alb_listener" "grpc" {
  load_balancer_arn = aws_lb.main.id
  port              = 50051
  protocol          = "HTTPS"

  certificate_arn = var.certificate_arn

  default_action {
    target_group_arn = aws_alb_target_group.grpc.id
    type             = "forward"
  }
}

# define target group to receive HTTPS traffic.
# the target group can then be references by the
# ECS service to receive traffic from the loadbalancer
resource "aws_alb_target_group" "grpc" {
  name                = "${var.name}-tg-${var.environment}-grpc"
  port                = 50051

  protocol            = "HTTP"
  protocol_version    = "GRPC"

  vpc_id      = aws_vpc.vpc.id
  target_type = "ip"

  health_check {
    healthy_threshold   = "3"
    interval            = "30"
    protocol            = "HTTP"
    matcher             = "12"
    timeout             = "3"
    path                = "/"
    unhealthy_threshold = "2"
  }
}