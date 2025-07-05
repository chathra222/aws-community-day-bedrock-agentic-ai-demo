import boto3
import subprocess
import os
from github import Github

def lambda_handler(event, context):
    logs = open('/tmp/failed_log.txt').read()
    dom_snapshot = open('/tmp/dom_snapshot.html').read() if os.path.exists('/tmp/dom_snapshot.html') else None
    test_file = open('/tmp/sample.spec.ts').read()

    bedrock = boto3.client('bedrock-agent-runtime')

    response = bedrock.invoke_agent(
        agentId=os.environ['AGENT_ID'],
        sessionId='playwright_self_heal',
        inputText=f"""
Logs:
{logs}

DOM Snapshot:
{dom_snapshot}

Test File:
{test_file}

Propose an updated test and return git diff.
""")
    fix = response['outputText']

    with open('/tmp/fix.diff', 'w') as f:
        f.write(fix)
    subprocess.run(['git', 'apply', '/tmp/fix.diff'], check=True)

    passed = subprocess.run(['npx', 'playwright', 'test'], capture_output=True).returncode == 0

    if passed:
        github = Github(os.environ['GITHUB_TOKEN'])
        repo = github.get_repo('YOUR_GITHUB_USER/YOUR_REPO')

        main = repo.get_branch('main')
        repo.create_git_ref(ref='refs/heads/self-heal', sha=main.commit.sha)

        subprocess.run(['git', 'checkout', '-b', 'self-heal'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Self-healed test'])
        subprocess.run(['git', 'push', '--set-upstream', 'origin', 'self-heal'])

        pr = repo.create_pull(
            title='Self-Healed Playwright Test',
            body='Fix proposed by Bedrock agent.',
            head='self-heal',
            base='main'
        )
        print(f"PR Created: {pr.html_url}")

    return {
        'fix_applied': passed
    }