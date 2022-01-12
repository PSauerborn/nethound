
# define ECS cluster
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.name}-cluster-${var.environment}"
}

# define ECS task run by service
resource "aws_ecs_task_definition" "grpc_server" {

  family                   = "${var.name}-service-grpc-${var.environment}"

  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  # define resouces for each task
  cpu                      = 256
  memory                   = 512

  # give task required permissions to access DB and
  # services running in private subnets
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name        = "${var.name}-container-grpc-${var.environment}"
    image       = "docker.alpinesoftware.net/nethound/grpc-server:${var.nethound_grpc_server_version}"
    essential   = true
    environment = [
      {
        "name": "PG_USER",
        "value": "${var.nethound_postgres_user}"
      },
      {
        "name": "PG_PASSWORD",
        "value": "${var.nethound_postgres_password}"
      },
      {
        "name": "PG_HOST",
        "value": "${var.postgres_host}"
      }
    ]
    repositoryCredentials = {
        "credentialsParameter": "arn:aws:secretsmanager:eu-west-1:717134789437:secret:docker/alpinesoftware/registry-5eoNqT"
    }
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "awslogs-nethound",
          "awslogs-region": "eu-west-1",
          "awslogs-stream-prefix": "nethound-grpc",
          "awslogs-create-group": "true"
        }
    }
    healthCheckGracePeriodSeconds = 60
    portMappings = [
          {
            protocol      = "tcp"
            containerPort = 50051
            hostPort      = 50051
          }
        ]
    }])
}

# define ECS task run by service
resource "aws_ecs_task_definition" "rest_server" {

  family                   = "${var.name}-service-rest-${var.environment}"

  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  # define resouces for each task
  cpu                      = 256
  memory                   = 512

  # give task required permissions to access DB and
  # services running in private subnets
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([{
    name        = "${var.name}-container-rest-${var.environment}"
    image       = "docker.alpinesoftware.net/nethound/rest-server:${var.nethound_rest_server_version}"
    essential   = true
    environment = [
      {
        "name": "PG_USER",
        "value": "${var.nethound_postgres_user}"
      },
      {
        "name": "PG_PASSWORD",
        "value": "${var.nethound_postgres_password}"
      },
      {
        "name": "PG_HOST",
        "value": "${var.postgres_host}"
      }
    ]
    repositoryCredentials = {
        "credentialsParameter": "arn:aws:secretsmanager:eu-west-1:717134789437:secret:docker/alpinesoftware/registry-5eoNqT"
    }
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "awslogs-nethound",
            "awslogs-region": "eu-west-1",
            "awslogs-stream-prefix": "nethound-rest",
            "awslogs-create-group": "true"
        }
    }
    healthCheckGracePeriodSeconds = 60
    portMappings = [
          {
              protocol      = "tcp"
              containerPort = 10456
              hostPort      = 10456
          }
        ]
    }])
}

# define ecs service to run ECS task via fargate
resource "aws_ecs_service" "ecs_service_rest" {

  name    = "${var.name}-service-rest-${var.environment}"
  cluster = aws_ecs_cluster.ecs_cluster.id

  # add container tasks to ecs service
  task_definition                    = aws_ecs_task_definition.rest_server.arn
  desired_count                      = 1
  launch_type                        = "FARGATE"
  scheduling_strategy                = "REPLICA"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = [aws_subnet.private_subnet.id]
    assign_public_ip = false
  }

  # attach ecs service to loadbalancer to control traffic
  load_balancer {
    target_group_arn = aws_alb_target_group.http.arn
    container_name   = "${var.name}-container-rest-${var.environment}"
    container_port   = 10456
  }
}

# define ecs service to run ECS task via fargate
resource "aws_ecs_service" "ecs_service_grpc" {

  name    = "${var.name}-service-grpc-${var.environment}"
  cluster = aws_ecs_cluster.ecs_cluster.id

  # add container tasks to ecs service
  task_definition                    = aws_ecs_task_definition.grpc_server.arn
  desired_count                      = 1
  launch_type                        = "FARGATE"
  scheduling_strategy                = "REPLICA"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = [aws_subnet.private_subnet.id]
    assign_public_ip = false
  }

  # attach ecs service to loadbalancer to control traffic
  load_balancer {
    target_group_arn = aws_alb_target_group.grpc.arn
    container_name   = "${var.name}-container-grpc-${var.environment}"
    container_port   = 50051
  }
}


resource "aws_security_group" "ecs_tasks" {
    name   = "${var.name}-sg-task-${var.environment}"
    vpc_id = aws_vpc.vpc.id

    ingress {
      protocol         = "tcp"
      from_port        = 50051
      to_port          = 50051
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }

    ingress {
      protocol         = "tcp"
      from_port        = 10456
      to_port          = 10456
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