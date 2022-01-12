
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.name}-ecsTaskRole"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.name}-ecsTaskExecutionRole"

  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "ecs-tasks.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_policy" "postgres" {
  name        = "${var.name}-task-policy-postgres"
  description = "Policy that allows access to PostgreSQL server"

 policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Effect": "Allow",
           "Action": [
               "rds-db:CreateTable",
               "rds-db:UpdateTimeToLive",
               "rds-db:PutItem",
               "rds-db:DescribeTable",
               "rds-db:ListTables",
               "rds-db:DeleteItem",
               "rds-db:GetItem",
               "rds-db:Scan",
               "rds-db:Query",
               "rds-db:UpdateItem",
               "rds-db:UpdateTable"
           ],
           "Resource": "arn:aws:rds:eu-west-1:717134789437:db:nethounddbpoc"
       }
   ]
}
EOF
}

# give ECS role access to postgres policy
resource "aws_iam_role_policy_attachment" "ecs_task_role_policy_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.postgres.arn
}


resource "aws_iam_policy" "reg_cred" {
  name        = "${var.name}-task-policy-reg-cred"
  description = "Policy that allows access to Alpine software container registry"

 policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
       {
           "Effect": "Allow",
           "Action": [
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecretVersionIds"
            ],
           "Resource": "arn:aws:secretsmanager:eu-west-1:717134789437:secret:docker/alpinesoftware/registry-5eoNqT"
       }
   ]
}
EOF
}

# give ECS role access to postgres policy
resource "aws_iam_role_policy_attachment" "reg_cred_secret_access" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.reg_cred.arn
}


resource "aws_iam_policy" "logs" {
  name        = "${var.name}-task-policy-logs"
  description = "Policy that allows access to log stream"

 policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
       {
            "Effect": "Allow",
            "Action": [
                "logs:GetLogEvents",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:PutRetentionPolicy",
                "logs:CreateLogGroup"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
   ]
}
EOF
}

# give ECS role access to postgres policy
resource "aws_iam_role_policy_attachment" "log_access" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.logs.arn
}