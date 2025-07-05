✅ 1️⃣ Wire up GitHub Actions Secrets
Your .github/workflows/ci.yml needs:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION (if needed)

GITHUB_TOKEN (PAT — Personal Access Token for PR creation)

🔑 How to do it:

In GitHub, go to your repo → Settings → Secrets and variables → Actions.

Click “New repository secret”.

Add:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

GITHUB_TOKEN (generate a classic token in your GitHub Account → Developer settings → Personal access tokens).

✅ Tip:
Give your PAT repo + workflow + contents permissions so the Lambda can push + PR.

✅ 2️⃣ Terraform Backend
Don’t store state locally — use S3 + DynamoDB for safe remote state.

Add this to your terraform/main.tf (top of file):

hcl
Copy
Edit
terraform {
  backend "s3" {
    bucket         = "YOUR-TF-STATE-BUCKET"
    key            = "playwright-self-heal-agent/terraform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "YOUR-TF-LOCK-TABLE"
    encrypt        = true
  }
}
✅ How to create S3 bucket & lock table:

bash
Copy
Edit
aws s3 mb s3://YOUR-TF-STATE-BUCKET
aws dynamodb create-table \
  --table-name YOUR-TF-LOCK-TABLE \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
✅ 3️⃣ Bedrock Agent & Lambda IAM Permissions
Ensure:

The Lambda role allows bedrock:InvokeAgent.

The Lambda has logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents.

Add inline to your IAM role:

hcl
Copy
Edit
resource "aws_iam_role_policy" "bedrock_invoke" {
  name = "BedrockInvokePolicy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "bedrock:InvokeAgent"
      ],
      Resource = "*"
    }]
  })
}
✅ 4️⃣ Git Branch + PR Handling
Your Lambda uses PyGithub.
✅ Be sure:

The PAT has repo scope.

The repo name is correct in handler.py:

python
Copy
Edit
repo = github.get_repo('YOUR_GITHUB_USER/YOUR_REPO')
✅ The branch main matches your default branch.

✅ 5️⃣ Deploy Lambda Correctly
When you terraform apply, you need to zip your handler:

bash
Copy
Edit
cd lambda
pip install -r requirements.txt -t .
zip -r lambda_function_payload.zip .
Copy the zip into terraform/ or adjust the filename path in main.tf accordingly.

✅ 6️⃣ Test the Flow
When all wired:
1️⃣ terraform init && terraform apply
2️⃣ Push a broken Playwright test → GitHub Actions runs → test fails
3️⃣ Action triggers Lambda → Bedrock fixes → tries new test → opens PR if passing.