import requests

from config import github_info


url = "https://api.github.com"

token = github_info["token"]
owner = github_info["user_name"]
repo  = github_info["repo_name"]


def get_pr(url, headers):
    url      += f"/repos/{owner}/{repo}/pulls"
    response  = requests.get(url = url, headers = headers).json()
    length    = len(response)

    return length

def 

headers = {"Accept": "application/vnd.github.v3+json"}

response = requests.get(url = url, headers = headers).json

print(res)