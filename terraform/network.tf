
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
}

######################################
# Private network interface definition
######################################

# create private AWS subnet for VPC/internal
# applications
resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = "eu-west-1a"
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route" "private_route" {
  # define route table definitions
  route_table_id         = aws_route_table.private_route_table.id
  # define destionation configurations
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main.id
}

resource "aws_route_table_association" "private_route_asc" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_nat_gateway" "main" {

  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet_alpha.id
  depends_on    = [aws_internet_gateway.gateway]
}


resource "aws_eip" "nat" {
  vpc = true
}

#####################################
# Public network interface definition
#####################################

# generate new AWS gateway for VPC to allow public
# traffic
resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.vpc.id
}

# create public AWS subnet for external applications
resource "aws_subnet" "public_subnet_alpha" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subnet_cidr_alpha
  availability_zone       = "eu-west-1a"

  map_public_ip_on_launch = true
}

# create public AWS subnet for external applications
resource "aws_subnet" "public_subnet_beta" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subnet_cidr_beta
  availability_zone       = "eu-west-1b"

  map_public_ip_on_launch = true
}

# create new route table to manange newtork rules
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id
}

# create new route to map traffic from internet
# gateway to route table
resource "aws_route" "public_route" {
  # define route table definitions
  route_table_id         = aws_route_table.public_route_table.id
  # define destionation configurations. note that
  # all networks are used for the the destination block
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.gateway.id
}

# create new association between public subnet and route table
resource "aws_route_table_association" "public_route_asc_a" {
  subnet_id      = aws_subnet.public_subnet_alpha.id
  route_table_id = aws_route_table.public_route_table.id
}

# create new association between public subnet and route table
resource "aws_route_table_association" "public_route_asc_b" {
  subnet_id      = aws_subnet.public_subnet_beta.id
  route_table_id = aws_route_table.public_route_table.id
}