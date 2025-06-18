output "bucket_name" {
  description = "Name of the Terraform state bucket"
  value       = aws_s3_bucket.tf_state.bucket
}

output "bucket_arn" {
  description = "ARN of the Terraform state bucket"
  value       = aws_s3_bucket.tf_state.arn
}