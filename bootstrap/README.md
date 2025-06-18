# Bootstrap Terraform Module

This module provisions the initial S3 bucket for storing Terraform state in an AWS account.

## Features

- Creates an S3 bucket for Terraform state storage
- Optionally enables versioning and encryption

## Prerequisites

- **AWS Credentials Configured**: A valid AWS Access Key ID and Secret Access Key (for an IAM user or role with permissions to create s3 buckets). These can be set via the AWS CLI (`aws configure`) or by exporting environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_PROFILE`).
- **Terraform Version**: `~> 1.9`

## Inputs

| Name            | Description                           | Type        | Default        | Required |
|-----------------|---------------------------------------|-------------|----------------|----------|
| bucket_name     | Name of the S3 bucket                 | string      | N/A            | yes      |
| region          | AWS Region                            | string      | `us-east-1`    | no       |
| tags            | Tags to apply to bucket               | map(string) | `{}`           | no       |
| enable_logging  | Enable access logging for the bucket  | bool        | `false`        | no       |
| log_bucket_name | S3 bucket to store access logs        | string      | `""`           | no       |

## Outputs

| Name         | Description                        |
|--------------|------------------------------------|
| bucket_name  | Name of the created S3 bucket      |
| bucket_arn   | ARN of the created S3 bucket       |

## Usage

```hcl
module "bootstrap" {
    source = "git::https://github.com/your-org/srl-terraform-modules.git//bootstrap"

    bucket_name = "my-terraform-state-bucket"
    # Add other variables as needed
}
```

## Notes

- `log_bucket_name` should be left blank (`""`) for initial creation for Terraform state bucket.

## Bootstrap Workflow

When you’re using the `bootstrap` module to create your Terraform state bucket, there’s a small “chicken-and-egg” dance:

1. **Initial Bootstrap Uses Local State**

   - Since the S3 bucket doesn’t exist yet, Terraform will default to storing state on your local disk.
   - Run the bootstrap module locally once to create the bucket.

2. **Configure Remote State Backend**

   - After you’ve created the bucket (`tf-state-srl-management`), update your Terragrunt project config to point at it:
     ```hcl
     # iac/root.hcl
     remote_state {
       backend = "s3"
       config = {
         bucket         = "tf-state-srl-management" # New bucket
         key            = "${path_relative_to_include()}/terraform.tfstate"
         region         = "us-east-1"
         # When ready, add your lock table:
         # dynamodb_table = "tf-state-locks"
       }
     }
     ```
   - Commit and merge this change (no apply required).

3. **Migrate Local State to S3**

   - Navigate into the bootstrap live folder:
     ```bash
     cd iac/live/bootstrap
     ```
   - Reinitialize with migration:
     ```bash
     terragrunt init
     ```
   - Terragrunt will detect the new backend and ask if you want to copy your local state to S3. Answer **yes**.
   - Verify in the S3 console that your state file now resides under `bootstrap/terraform.tfstate`.

### Quick Commands

```bash
# 1. Bootstrap creates bucket with local state
cd iac/live/bootstrap
terragrunt init
terragrunt apply

# 2. Configure remote backend s3 state bucket in project.hcl (commit + merge)

# 3. Migrate local state to S3
cd iac/live/bootstrap
terragrunt init   # choose "yes" to migrate
```

Now all future IaC will store its state in S3, ensuring centralized, durable, and safe state management.

