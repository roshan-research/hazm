## Contribution

Before you start development, open a new issue and discuss your idea with a team member. Make sure you have a clear agreement on the approach or a written and approved spec. Then follow these steps:

1. If you are not a team member, fork the repo and clone it to your local machine. If you are a team member, clone the repo directly without forking.

2. Create a feature branch with this name format: `users/<username>/<description>`. For example: `users/ayub/migrate-py2-to-py3`.

3. Make and commit changes to your feature branch.

4. Create a pull request from your feature branch to the main branch and fill out the details.

5. Wait for someone to review your PR and provide feedback.

6. Address the review comments by making changes in your feature branch and pushing them back.

7. After your PR is approved, an authorized team member (maybe you yourself) will merge it into the main branch and delete your feature branch. It's recommended to delete your feature branch from your local machine to keep your repository clean and avoid confusion.

8. Sync your local main branch with the remote main branch using git checkout main && git pull.

9. Keep making changes to the code using new feature branches as described above, if you like.

Thank you for your contribution! 😍

## Rules

1. **Follow the pattern of what you already see in the code**. This is our [coding style guide](./CODING.md).

2. **Make atomic commits**: each commit should contain a single logical change that can be easily understood and reverted if needed. Avoid making large or unrelated changes in one commit. If you find it difficult to come up with a brief and clear commit message, it could be a sign that your changes are too large or not related to each other. It's recommended to split them into smaller, logical chunks and make separate commits for better code management and collaboration.


3. **Use new feature branches for every change**: create a new feature branch from the main branch for each new feature or bug fix that you want to contribute. Do not work directly on the main branch or reuse old feature branches.

