import requests
import csv

USERNAME = 'danielrosehill'
url = f'https://api.github.com/users/{USERNAME}/repos'
response = requests.get(url)

if response.status_code == 200:
    repos = response.json()
    csv_data = []

    for repo in repos:
        if not repo['private']:
            repo_name = repo['name']
            repo_url = repo['html_url']
            csv_data.append([repo_name, repo_url])
    
    with open('github_repos.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Repository Name', 'URL'])
        csvwriter.writerows(csv_data)

    print('CSV file "github_repos.csv" created successfully.')
else:
    print(f'Failed to retrieve repositories: {response.status_code}')
