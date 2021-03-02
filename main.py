import json
import requests

from config import token


def check_pr(modified_file):
    return True if modified_file == "pr_file.py" else False


def accept_merge(url, headers, base, head):
    body = {"base": base, "head": head}
    response = requests.post(
        url     = url,
        headers = headers,
        data    = json.dumps(body)
    ).json()

    return response


def lambda_handler(event, context):
    data     = json.loads(event["body"])
    url      = data["repository"]["merges_url"]
    headers  = {
        "Accept"       : "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    base     = "origin"     
    commits  = data["commits"]
    
    for commit in commits:
        modified_file = commit["modified"][0]
        head          = commit["id"]
        committer     = commit["committer"]["name"]
        if check_pr(modified_file):
            response  = accept_merge(url, headers, base, head)
            print(response)
        else:
            print(f"{committer} merge unaccepted, change the another file.")

    return {
        "status_code": 400,
        "body"       : json.dumps("You can only change the pr_file.py")
    }