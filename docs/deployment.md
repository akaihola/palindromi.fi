# Deployment

Current operating instructions, 2026-10-19.

Antti owns publishing and deployment. A push to `main` triggers
`.github/workflows/deploy.yaml`, which installs frozen production dependencies
with uv and Python 3.11, runs `make build`, uploads `html/` as a Pages artifact,
and deploys it with `actions/deploy-pages`. A local merge does not publish.
Local builds and previews need no GitHub credentials.

All four jobs across Deploy, Linting and Formatting currently pin Ubuntu 24.04.
Task [11](tasks/11-validate-ubuntu-26-workflows-and-remove-ubuntu-24-04-pins.md)
owns Ubuntu 26 validation and pin removal. Keep that work separate.

Linting and Formatting run on main pushes and pull requests. They check changed
Python code against `origin/main...`; they do not run tests or build the site on
pull requests. Run the README's local build and pytest commands before handing
changes back. The architecture review's draft B proposes that missing CI coverage.

Follow the current task's publishing constraints. Task 15 explicitly forbids
pushing or deploying, so completion stops at a local merge to `main`. Historical
notes that say no deployment guide exists predate this file.
