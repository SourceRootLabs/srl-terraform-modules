variable "bucket_name" {
  description = "Name of the S3 bucket for storing Terraform state."
  type        = string
}

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "Tags to apply to bucket."
  type        = map(string)
  default     = {}
}

variable "enable_logging" {
  description = "Enable access logging for the bucket."
  type        = bool
  default     = false
}

variable "log_bucket_name" {
  description = "The name of the S3 bucket to store access logs."
  type        = string
  default     = ""
}
