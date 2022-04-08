provider "aws" {
  region     = "us-west-2"
  access_key = var.aws_key
  secret_key = var.aws_secret
  version    = "~> 3.48"
}

data "aws_ami" "app_ami" {
  most_recent = true
  owners = ["099720109477"]


  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bioni*"]
  }
 }

resource "aws_instance" "prod" {
    ami = data.aws_ami.app_ami.id
    instance_type = "t2.medium"
    key_name      = "keypair"
    vpc_security_group_ids = [aws_security_group.dynamicsg.id]

provisioner "remote-exec" {
     inline = [
       "sudo apt-get update",
       "curl -Os https://downloads.thousandeyes.com/agent/install_thousandeyes.sh",
       "chmod +x install_thousandeyes.sh",
       "sudo ./install_thousandeyes.sh -b -l /var/log TE API KEY"
     ]
   }
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("./terra2.pem")
      host        = self.public_ip
      agent = false
    }
  }


   
variable "sg_ports" {
  type        = list(number)
  description = "list of ingress ports"
  default     = [22]
}

resource "aws_security_group" "dynamicsg" {
  name        = "dynamic-sg"
  description = "Ingress for Vault"

  dynamic "ingress" {
    for_each = var.sg_ports
    iterator = port
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
