
variable "aws_access_key" {
    type = string
}

variable "aws_secret_key" {
    type = string
}

variable "aws_region" {
    type    = string
    default = "eu-west-1"
}

variable "vpc_cidr" {
    type    = string
    default = "10.0.0.0/16"
}

variable "private_subnet_cidr" {
    type    = string
    default = "10.0.1.0/24"
}

variable "public_subnet_cidr_alpha" {
    type    = string
    default = "10.0.2.0/24"
}

variable "public_subnet_cidr_beta" {
    type    = string
    default = "10.0.3.0/24"
}

variable "postgres_username" {
    type    = string
    default = "postgres"
}

variable "postgres_password" {
    type    = string
}

variable "postgres_host" {
    type    = string
    default = "nethounddbpoc.c4pnpikv2bqm.eu-west-1.rds.amazonaws.com"
}

variable "name" {
    type    = string
    default = "nethound"
}

variable "environment" {
    type    = string
    default = "poc"
}

variable "certificate_arn" {
    type    = string
    default = "arn:aws:acm:eu-west-1:717134789437:certificate/96685fde-1c9a-455d-b2b3-991ee43ac881"
}

variable "nethound_postgres_user" {
    type    = string
    default = "nethound"
}

variable "nethound_postgres_password" {
    type    = string
}