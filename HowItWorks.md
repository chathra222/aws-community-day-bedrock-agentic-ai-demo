📌 What does the Playwright Self-Heal Agent do?
Think of it like a smart virtual QA engineer that:
1️⃣ Watches for failed end-to-end (E2E) tests.
2️⃣ Analyzes the reason they failed.
3️⃣ Proposes a working fix — automatically.
4️⃣ Validates the fix.
5️⃣ Creates a Pull Request (PR) for human review.

✅ Here’s exactly what it does, in real steps

1️⃣ Detects Playwright test failures
The agent is triggered by your CI/CD pipeline.
When npx playwright test fails in GitHub Actions → your workflow calls the agent orchestration (via Lambda).

2️⃣ Gathers all needed debugging context
Takes:

The error logs (failed_log.txt)

The DOM snapshot at failure time (dom_snapshot.html)

The original test file (sample.spec.ts)

3️⃣ Uses AI (Bedrock LLM) to understand the failure
Parses the logs:

What step failed?

What selector broke?

Looks at the DOM snapshot:

Did the HTML change?

Did a button label change?

Looks at the test code:

Which line needs to change?

4️⃣ Proposes a fix
The LLM writes:

An updated selector.

A new Playwright command.

A Git diff that shows exactly what changed.

Example:

diff
Copy
Edit
- await page.locator('button.submit').click();
+ await page.getByTestId('login-button').click();
5️⃣ Runs the fix safely
The agent orchestration uses a Lambda function to:

Apply the diff.

Re-run the test locally in a sandbox.

Check if the fix works.

If it passes, the agent knows the fix is valid.

6️⃣ Creates a new Pull Request
If the fix works, the agent:

Creates a new branch.

Commits the updated test file.

Pushes the branch.

Opens a GitHub PR.

Adds a comment with an explanation:
“This test was updated to fix a broken selector that failed due to a DOM change. Please review and merge.”

✅ So what does the agent not do?
It doesn’t blindly merge the fix.

It doesn’t test business logic — it only updates the failing Playwright script.

It relies on your CI/CD for final validation.