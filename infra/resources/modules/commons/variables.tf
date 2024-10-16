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

variable "cidr_onboarding_fn" {
  type        = list(string)
  description = "The subscription function address space"
}
variable "cidr_ask_bot_fn" {
  type        = list(string)
  description = "The subscription function address space"
}
variable "function_onboarding_config" {
  type = object({
    kind              = string
    sku_tier          = string
    sku_size          = string
    autoscale_minimum = number
    autoscale_maximum = number
    autoscale_default = number
  })
  default = {
    kind              = "Linux"
    sku_tier          = "PremiumV3"
    sku_size          = "P1v3"
    autoscale_minimum = 1
    autoscale_maximum = 30
    autoscale_default = 1
  }
}
