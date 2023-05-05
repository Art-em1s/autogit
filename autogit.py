import requests
import os
from git import Repo
import time



def get_all_user_repos(token):
    url = f"https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    repos = []
    page = 1

    while True:
        response = requests.get(f"{url}?page={page}&per_page=100", headers=headers)

        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            break

        if not response.json():
            break

        repos.extend(response.json())
        page += 1

    return repos


def clone_or_pull_repos(token, dest_dir):
    start_time = time.time()
    repos = get_all_user_repos(token)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for repo in repos:
        repo_url = repo["clone_url"]
        repo_name = repo["name"]
        owner_name = repo["owner"]["login"]
        owner_path = os.path.join(dest_dir, owner_name)
        repo_path = os.path.join(owner_path, repo_name)

        if not os.path.exists(owner_path):
            os.makedirs(owner_path)

        if not os.path.exists(repo_path):
            print(f"Cloning {repo_url} to {repo_path}")
            Repo.clone_from(repo_url, repo_path)
        else:
            print(f"Updating {repo_url} in {repo_path}")
            local_repo = Repo(repo_path)
            try:
                local_repo.git.pull()
            except Exception as e:
                print(f"Error updating {repo_name}: {e}")

    end_time = time.time()
    total_time = end_time - start_time
    minutes, seconds = divmod(total_time, 60)
    seconds = round(seconds, 3)

    print("Execution time: {:d}:{:06.3f}".format(int(minutes), seconds))


# Replace these with the appropriate values
github_token = "your-personal-access-token"
destination_directory = "path-to-destination-directory"

clone_or_pull_repos(github_token, destination_directory)