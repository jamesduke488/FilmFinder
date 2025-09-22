variable "aws_region" { 
    type = string  
    default = "eu-west-1" 
}

variable "project_name"     { 
    type = string  
    default = "film-finder" 
}

variable "artifact_key" {
    type = string
    default = null 
} # set by CI (e.g. lambda_2025-09-11.zip)