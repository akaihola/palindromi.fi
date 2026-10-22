# Deployment

Current operating instructions, 2026-10-22; hosted validation status below
comes from the recorded October 21 results.

Antti owns publishing and deployment. A push to `main` triggers
the [Deploy workflow], which installs frozen production dependencies
with uv and Python 3.11, runs `make build`, uploads the [rendered site] as a Pages artifact,
and deploys it with `actions/deploy-pages`. A local merge does not publish.
Local builds and previews need no GitHub credentials.

All four jobs across Deploy, Linting and Formatting now pin Ubuntu 26.04.
[Ubuntu 26 workflow validation] records successful Formatting, Linting and
build-only runs on image `20261012.163.1`, including Transcrypt compilation
and site rendering. Deployment on main with these pins remains pending
Antti's push and a successful Deploy run. A local merge does not verify it.

The [Linting] and [Formatting] workflows run on main pushes and pull requests.
They check changed
Python code against `origin/main...`; they do not run tests or build the site on
pull requests. Run the [local checks] before handing changes back.
The [architecture review]'s draft B proposes that missing CI coverage.

Follow the current task's publishing constraints. A local merge and local checks
do not authorize a push or deployment.

[Deploy workflow]: ../.github/workflows/deploy.yaml
[rendered site]: ../html/
[Ubuntu 26 workflow validation]: tasks/11-validate-ubuntu-26-workflows-and-remove-ubuntu-24-04-pins.md
[Linting]: ../.github/workflows/linting.yaml
[Formatting]: ../.github/workflows/formatting.yaml
[local checks]: development.md#tests-and-incremental-checks
[architecture review]: reviews/2026-10-19-architecture-review.md
