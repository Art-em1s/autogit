# AutoGit

This Node.js script clones or updates all repositories that the authenticated user has access to, including public, private, and organization repositories. The repositories are organized into separate folders based on the owner (organization or user) in the destination directory.

## Dependencies

- [Node.js](https://nodejs.org/en/download)

You can install these dependencies using the following command:

```bash
npm install
```

## Setup

1. Generate a GitHub personal access token:
    - Go to https://github.com/settings/tokens
    - Click "Generate new token"
    - Give your token a name and check the necessary scopes, e.g., `repo`, `user`
    - Click "Generate token" and copy the generated token

2. Replace the placeholder values in the script:
    - Replace `'your-personal-access-token'` with your generated GitHub personal access token
    - Replace `'path-to-destination-directory'` with the path to the directory where you want to clone or update the repositories

## Usage

Simply run the script:

```bash
npm start
```

The script will clone or update all repositories that the authenticated user has access to and organize them into separate folders based on the owner (organization or user) in the destination directory.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
