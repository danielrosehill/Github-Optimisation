import requests
import csv

def get_github_repositories(username, token):
    # Define the URL for the GitHub API
    url = f"https://api.github.com/user/repos"
    
    # Headers for the request, including the authorization token
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Parameters to get all repositories
    params = {
        "visibility": "all",
        "affiliation": "owner"
    }
    
    # Make the request to the GitHub API
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return None

def save_repos_to_csv(repositories, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Visibility"])
        
        for repo in repositories:
            visibility = "Private" if repo["private"] else "Public"
            writer.writerow([repo["name"], visibility])

# Replace 'your_github_username' with your GitHub username
# Replace 'your_github_token' with your personal access token
username = "aaaaa"
token = "sfsfsfsfsfsfsf"

repos = get_github_repositories(username, token)
if repos:
    save_repos_to_csv(repos, "github_repositories.csv")
    print("Repositories have been saved to 'github_repositories.csv'")
