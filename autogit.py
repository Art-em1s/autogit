import requests
import os
from git import Repo
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor


def time_delta(epoch1, epoch2):
    delta = timedelta(seconds=epoch2 - epoch1)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d} hours, {minutes:02d} minutes, {seconds:02d} seconds"
    elif minutes > 0:
        return f"{minutes:02d} minutes, {seconds:02d} seconds"
    else:
        return f"{seconds:02d} seconds"


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


def clone_or_pull_repo(repo, dest_dir):
    repo_url = repo["clone_url"]
    repo_name = repo["name"]
    owner_name = repo["owner"]["login"]
    owner_path = os.path.join(dest_dir, owner_name)
    repo_path = os.path.join(owner_path, repo_name)

    if not os.path.exists(owner_path):
        os.makedirs(owner_path)

    if not os.path.exists(repo_path):
        print(f"Cloning {owner_name}/{repo_name} to {repo_path}")
        Repo.clone_from(repo_url, repo_path)
    else:
        try:
            local_repo = Repo(repo_path)
            active_branch = local_repo.active_branch
            local_commit = local_repo.commit(active_branch)
            
            remote = local_repo.remote()
            remote.fetch()
            remote_commit = remote.refs[active_branch.name].commit

            # If the local commit is the same as the remote commit, we don't need to update
            if local_commit.hexsha == remote_commit.hexsha:
                print(f"Skipping {owner_name}/{repo_name}, already up to date")
                return
            
            print(f"Updating {owner_name}/{repo_name} in {repo_path}")
            local_repo.git.pull()
        except Exception as e:
            print(f"Error updating {owner_name}/{repo_name}: {e}")
            return


def spawn_threads(token, dest_dir, max_workers=5):
    start_time = time.time()
    repos = get_all_user_repos(token)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [executor.submit(clone_or_pull_repo, repo, dest_dir) for repo in repos]
        for future in tasks:
            future.result()

    print(f"Execution time: {time_delta(start_time, time.time())}")


# Replace these with the appropriate values
github_token = "your-personal-access-token"
destination_directory = "path-to-destination-directory"
max_workers = 5 # Number of threads to spawn, 10 seems to cause issues with GitHub rate limiting(?)

spawn_threads(github_token, destination_directory, max_workers)
