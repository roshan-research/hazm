## Contribution Guideline

Thank you for your interest in contributing to our project. Please follow these steps:

1. (**Optional but recommended**) Open an issue and discuss your idea to avoid effort on something that may not be accepted.
2. Fork and clone the repo.
3. Install [poetry](https://python-poetry.org/) if you haven't already.
4. Run `poetry update --with docs, dev`.
5. Work on your changes using `python 3.8.0` and follow [coding style guide](./CODING.md).
6. Run `poetry run poe lint` and fix linting errors.
7. Run `poetry run poe test` and fix any failing tests.
8. push & pull request and link to the issue  (if any).
9. Keep in touch with reviewers until merge.

Thank you for your contribution! 😍

## Rules

1. Follow the pattern of what you already see in the code. 
2. Follow [coding style guide](./CODING.md).
2. Make atomic commits, one change per commit. Split large or unrelated changes into smaller commits.
