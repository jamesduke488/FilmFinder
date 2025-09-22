variable "aws_region"       { type = string  default = "eu-west-1" }
variable "project_name"     { type = string  default = "film-finder" }
variable "artifact_bucket"  { type = string }
variable "artifact_key"     { type = string } # set by CI (e.g. lambda_2025-09-11.zip)