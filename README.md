# Playwright Self-Heal Agent


## Setup

1. Deploy with Terraform.
2. Push tests.
3. CI runs Playwright.
4. On failure, Lambda fixes and PRs.

## Requirements

- AWS account with Bedrock + Lambda.
- GitHub repo with PAT token.