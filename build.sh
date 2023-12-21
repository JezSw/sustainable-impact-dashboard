#!/bin/bash
REPO_NAME='ukaea-impact-dashboard'

if [ ! -d "${REPO_NAME}" ]; then
    echo "No instance of ${REPO_NAME}, creating with defaults."
    cookieninja -f --no-input .
    cp github.token ${REPO_NAME}
    cp sources.json ${REPO_NAME}
else
    echo "Found previous instance of ${REPO_NAME}, replaying for new content."
    cookieninja -f --replay .
fi

pushd ${REPO_NAME}

if [ ! -d "venv" ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi

#step 1 search for relevant packages on pypi and githib
venv/bin/python get_github_repos.py
#update stats 
venv/bin/python update_github_stats.py
#get coverage/docs/etc badges
venv/bin/python get_loc.py
venv/bin/python get_badges.py
#update html files
venv/bin/python update_dashboard.py

popd