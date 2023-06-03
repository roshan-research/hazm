## Contribution Guideline

Thank you for your interest in contributing to our project. Please follow these steps:

1. (**Optional but recommended, especially for big changes**) Create an issue and let's discuss your idea to avoid wasting time on something that we may not accept.
2. Fork and clone the repo. 
3. Install poetry and run `poetry update --with docs, dev`.
4. Work on your changes in your fork. Follow the [coding style guide](./CODING.md) and conventions (if any).
5. Run `poetry run poe lint` and `poetry run poe test` and fix any possible issues.
6. Commit and push your changes. Open a pull request and link to the issue.
7. Resolve conflicts and address feedback from reviewers. Keep in touch with them until they merge your pull request.

Thank you for your contribution! 😍

## Rules

1. **Follow the pattern of what you already see in the code**. This is our [coding style guide](./CODING.md).

2. **Make atomic commits**: each commit should contain a single logical change that can be easily understood and reverted if needed. Avoid making large or unrelated changes in one commit. If you find it difficult to come up with a brief and clear commit message, it could be a sign that your changes are too large or not related to each other. It's recommended to split them into smaller, logical chunks and make separate commits for better code management and collaboration.
