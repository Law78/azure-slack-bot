variable "prefix" {
  type    = string
  default = "io-sm"
  validation {
    condition = (
      length(var.prefix) < 6
    )
    error_message = "Max length is 6 chars."
  }
}

variable "env_short" {
  type = string
  validation {
    condition = (
      length(var.env_short) <= 1
    )
    error_message = "Max length is 1 chars."
  }
}

variable "location" {
  type    = string
  default = "italynorth"
}

variable "location_short" {
  type    = string
  default = "itn"
}

variable "tags" {
  type = map(any)
  default = {
    CreatedBy = "Terraform"
  }
}