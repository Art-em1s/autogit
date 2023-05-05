const axios = require('axios');
const fs = require('fs');
const path = require('path');
const simpleGit = require('simple-git');

async function get_all_user_repos(token) {
    const url = "https://api.github.com/user/repos";
    const headers = { Authorization: `token ${token}` };
    const repos = [];
    let page = 1;

    while (true) {
        try {
            const response = await axios.get(`${url}?page=${page}&per_page=100`, { headers });

            if (response.status !== 200) {
                console.log(`Error fetching repositories: ${response.status}`);
                break;
            }

            if (response.data.length === 0) {
                break;
            }

            repos.push(...response.data);
            page += 1;
        } catch (error) {
            console.log(`Error fetching repositories: ${error}`);
            break;
        }
    }

    return repos;
}

async function clone_or_pull_repos(token, dest_dir) {
	console.time('Execution time: ');
    const repos = await get_all_user_repos(token);

    if (!fs.existsSync(dest_dir)) {
        fs.mkdirSync(dest_dir, { recursive: true });
    }

	const finishedRepos = await Promise.all(repos.map(async (repo) => {
        const repo_url = repo.clone_url;
        const repo_name = repo.name;
        const owner_name = repo.owner.login;
        const owner_path = path.join(dest_dir, owner_name);
        const repo_path = path.join(owner_path, repo_name);

        if (!fs.existsSync(owner_path)) {
            fs.mkdirSync(owner_path, { recursive: true });
        }

        const git = simpleGit();

        if (!fs.existsSync(repo_path)) {
            console.log(`Cloning ${repo_url} to ${repo_path}`);
            await git.clone(repo_url, repo_path);
        } else {
            console.log(`Updating ${repo_url} in ${repo_path}`);
            try {
                const localRepo = simpleGit(repo_path);
                await localRepo.pull();
            } catch (error) {
                console.log(`Error updating ${repo_name}: ${error}`);

				return 0;
            }
        }

		return 1;
    }));

	const finishedReposCount = finishedRepos?.filter((repo) => repo === 1).length;

	console.log(`Finished updating or cloning ${finishedReposCount} repositories!`);
	console.timeEnd('Execution time: ');
}

// Replace these with the appropriate values
const github_token = 'your-personal-access-token';
const destination_directory = 'path-to-destination-directory';

clone_or_pull_repos(github_token, destination_directory);
