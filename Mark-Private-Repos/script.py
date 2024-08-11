import os
import requests
import subprocess

# Replace with your GitHub username and token
GITHUB_USERNAME = 'your_username'
GITHUB_TOKEN = 'your_token'

# Path to your local Git repositories
GIT_FOLDER_PATH = '/path/to/your/git/folder'

# Function to extract the repository name from the remote URL
def get_repo_name(repo_path):
    try:
        # Get the remote URL
        remote_url = subprocess.check_output(
            ['git', '-C', repo_path, 'config', '--get', 'remote.origin.url'],
            universal_newlines=True
        ).strip()
        
        # Extract the repository name from the URL
        if remote_url.startswith('https://') or remote_url.startswith('http://'):
            repo_name = remote_url.split('/')[-1].replace('.git', '')
        elif remote_url.startswith('git@'):
            repo_name = remote_url.split(':')[-1].split('/')[-1].replace('.git', '')
        else:
            return None

        return repo_name
    except subprocess.CalledProcessError:
        return None

# Function to check if a repository is private
def is_repo_private(repo_name):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}'
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 200:
        return response.json()['private']
    else:
        return None

# Generate the markdown report
report_lines = []

for repo in os.listdir(GIT_FOLDER_PATH):
    repo_path = os.path.join(GIT_FOLDER_PATH, repo)
    if os.path.isdir(repo_path):
        repo_name = get_repo_name(repo_path)
        if repo_name:
            private_status = is_repo_private(repo_name)
            if private_status is not None:
                status = 'PRIVATE' if private_status else 'PUBLIC'
                report_lines.append(f'{repo_path} - {status}')
            else:
                report_lines.append(f'{repo_path} - Could not determine the status')
        else:
            report_lines.append(f'{repo_path} - Not a valid Git repository')

# Write the report to a markdown file
report_file_path = os.path.join(os.getcwd(), 'repo_report.md')
with open(report_file_path, 'w') as report_file:
    report_file.write('\n'.join(report_lines))

print(f'Report generated: {report_file_path}')
