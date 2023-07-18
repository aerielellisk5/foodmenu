terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}


resource "aws_instance" "foodmenu_app" {
  ami           = "ami-069d73f3235b535bd"
  instance_type = "t2.micro"

  tags = {
    Name = "HelloWorld"
  }
}


resource "aws_vpc" "foodmenu_vpc" {
  cidr_block =  "10.0.0.0/16"
  tags = {
    name = "production_vpc"
  }
}

resource "aws_subnet" "foodmenu_subnet1" {
  vpc_id = "aws_vpc.foodmenu_vpc"
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-2a"
  tags = {
    name = "foodmenu_subnet1"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.foodmenu_vpc.id

  tags = {
    Name = "main"
  }
}

resource "aws_route_table" "foodmenu_rt" {
  vpc_id = aws_vpc.foodmenu_vpc.id

  route {
    cidr_block = "0.0.0.0"
    gateway_id = aws_internet_gateway.aws_internet_gateway.gw.id
  }

  route {
    ipv6_cidr_block        = "::/0"
    egress_only_gateway_id = aws_internet_gateway.aws_internet_gateway.gw.id
  }

  tags = {
    Name = "foodmenu_rt"
  }
}

resource "aws_route_table_association" "food_menu_rt_association" {
  subnet_id      = aws_subnet.foodmenu_subnet1.id
  route_table_id = aws_route_table.foodmenu_rt.id
}

resource "aws_security_group" "allow_web" {
  name        = "allow web traffic"
  description = "Allow web inbound traffic"
  vpc_id      = aws_vpc.foodmenu_vpc.id

  ingress {
    description      = "HTTPS"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "HTTP"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "ssh"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "allow_web"
  }
}

resource "aws_network_interface" "foodmenu_webserver_nic" {
  subnet_id       = aws_subnet.foodmenu_subnet1.id
  private_ips     = ["10.0.1.50"]
  security_groups = [aws_security_group.allow_web]

  # attachment {
  #   instance     = aws_instance.test.id
  #   device_index = 1
  # }
}

# need to assign it a public ip address

resource "aws_eip" "one" {
  vpc                       = true
  network_interface         = "aws_network_interface.foodmenu_webserver_nic"
  associate_with_private_ip = "10.0.1.50"
  depends_on = ["aws_internet_gateway.gw"]
}

# data "aws_ami" "ubuntu" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
#   }

#   filter {
#     name   = "virtualization-type"
#     values = ["hvm"]
#   }

#   owners = ["099720109477"] # Canonical
# }

# resource "aws_instance" "web" {
#   ami           = "${data.aws_ami.ubuntu.id}"
#   instance_type = "t2.micro"

#   tags = {
#     Name = "HelloWorld"
#   }
# }
