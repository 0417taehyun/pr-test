import json
import requests

from config import token


def accept_merge(url, headers):
    url      += "/merge"
    body      = {"commit_title": "Merge Accepted"}
    content   = "Merge 완료!"
    response  = requests.put(url = url, headers = headers, data = body)

    if response.status_code == 409:
        content = "Conflict를 해결해주세요!"

    return content


def check_file(url, headers):
    url      += "/files"
    response  = requests.get(url = url, headers = headers).json()
    print(response)

    file = response[0]["filname"]
    if file != "pr_file.py":
        return False

    print(response[0]["patch"])


def create_review(url, headers, content):
    url     += "/reviews"
    body     = {"body": content}
    response = requests.post(
        url     = url,
        headers = headers,
        data    =  json.dumps(body)
    )

    return response.status_code


def lambda_handler(event, context):
    headers    = {
        "Accept"       : "application/vnd.github.v3+json",
        "Content-Type" : "application/json; charset=utf-8",
        "Authorization": f"token {token}",
    }
    data = json.loads(event["body"])

    commit_count        = data["pull_request"]["commits"]
    changed_files_count = data["pull_request"]["changed_files"]
    pull_request_url    = data["pull_request"]["_links"]["self"]["href"]

    if commit_count > 2:
        content  = "git rebase를 통해 commit을 정리해주세요 :)"
        response = create_review(pull_request_url, headers, content)
        print(response)
        return False

    if changed_files_count > 2:
        content  = "pr_file.py 파일만 수정하실 수 있습니다!"
        response = create_review(pull_request_url, headers, content)
        print(response)
        return False

    print(check_file(pull_request_url, headers))

    content  = accept_merge(pull_request_url, headers)
    response = create_review(pull_request_url, headers, content)
    print(response)