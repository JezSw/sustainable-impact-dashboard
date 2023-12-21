import json
from github import Github
from github.GithubException import RateLimitExceededException

from sksurgerystats.common import add_github_package
from sksurgerystats.from_github import get_token

token = None
token = get_token()

if token is not None:
    g = Github(token)
    with open('sources.json', 'r') as sources_file:
        sources_json = json.load(sources_file)
        for source in sources_json['sources']:
            if source['type'] == 'org':
                org = g.get_organization(source['path'])
                reps = org.get_repos()

                try:
                    for rep in reps:
                        add_github_package(rep)
                except RateLimitExceededException:
                    print("Got a rate limit exception from Github, probably because ",
                        "your search term returned too many matches. ",
                        "I've halted adding new libraries from GitHub")
            else:
                repo = g.get_repo(source['path'])
                try:
                    add_github_package(repo)
                except RateLimitExceededException:
                    print("Got a rate limit exception from Github, probably because ",
                        "your search term returned too many matches. ",
                        "I've halted adding new libraries from GitHub")
