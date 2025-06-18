# Random Pet Module

This module is designed to assist in testing and validating Terraform or Terragrunt configurations. It leverages the `random_pet` resource to generate a unique, human-readable name on each run.

Although this module does not provision any actual infrastructure resources, it performs all the key steps of a typical Terraform workflow—initialization, planning, application, state management, and output generation. This makes it useful for verifying that:

- Your Terraform or Terragrunt backend is configured correctly.
- Remote state storage (e.g., in S3, GCS, etc.) is working as expected.
- Module sourcing and dependencies are properly resolved.
- Workspace or environment-specific settings are applied successfully.

By using this lightweight module, you can confirm that your infrastructure-as-code tooling is operational without incurring any cloud costs or requiring access to provider credentials.