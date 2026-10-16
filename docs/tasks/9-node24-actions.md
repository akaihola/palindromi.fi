---
depends-on: [6, 7, 8]
---

# Move the workflows to action versions that run on Node.js 24

GitHub deprecated Node.js 20 for actions
(https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/).
Runners already force these actions onto Node.js 24 and annotate every run with a
warning. The runs on `010167c` (2026-10-06) named:

- Deploy: `actions/checkout@v4`, `actions/setup-python@v5`, and
  `actions/upload-artifact@v4`, which `actions/upload-pages-artifact@v3` calls.
- Linting and Formatting: `actions/checkout@v3`, `actions/setup-python@v4`.

Tasks 6 to 8 may replace or re-pin some of these, so start from the workflows as they
stand after those tasks. For each action, move to the newest major release whose
`action.yml` declares `runs.using: node24`. For composite actions, check the actions
they call. Do the same for anything new that tasks 6 to 8 added, such as
`astral-sh/setup-uv`.

Done when runs of all three workflows show no Node.js 20 annotation and the site
still deploys.

## Implementation and local validation, 2026-10-15

Tasks 6 to 8 are accepted. Their workflows already replaced setup-python with
`astral-sh/setup-uv@v10.2.0`. Keep that pin: its
[action.yml](https://github.com/astral-sh/setup-uv/blob/v10.2.0/action.yml)
declares `node24` for both setup and cache cleanup, and v10 remains the newest
major release.

Updated all three workflows to `actions/checkout@v7`, Deploy to
`actions/upload-pages-artifact@v5` and `actions/deploy-pages@v5`. GitHub's latest
release endpoints reported checkout v7.0.1, upload-pages-artifact v5.0.0 and
deploy-pages v5.0.1. Their action manifests were checked directly:

- [checkout v7](https://github.com/actions/checkout/blob/v7/action.yml): `node24`.
- [deploy-pages v5](https://github.com/actions/deploy-pages/blob/v5/action.yml):
  `node24`.
- [upload-pages-artifact v5](https://github.com/actions/upload-pages-artifact/blob/v5/action.yml):
  composite, calling upload-artifact at SHA
  `bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`, labelled v7.0.0.
- [That upload-artifact manifest](https://github.com/actions/upload-artifact/blob/bbbca2ddaa5d8feaa63e36b76fdaad77386f024f/action.yml):
  `node24`; v7 remains its newest major release.

A recursive audit of every workflow's `uses` steps and the composite's children
passed for all five distinct actions. Actionlint v1.7.12 passed without
exclusions. A frozen production install on CPython 3.11.16 and the exact Deploy
build command, `uv run --no-sync --no-dev make build`, both passed.
`git diff --check` passed. No application code or dependency lock changed.

Remote validation is blocked. The user authorized publishing local main,
including the six earlier unpublished commits, on 2026-10-15. The push was
rejected by GitHub because the configured Personal Access Token lacks the
`workflow` scope required to update `.github/workflows/deploy.yaml`. Existing
SSH credentials also failed with `Permission denied (publickey)`. No remote
workflow run or deployment was triggered.

Keep task 9 In Progress until credentials permit the push, Deploy, Formatting
and Linting all pass without Node.js 20 annotations, and the deployed site is
checked. No deployment guide exists; a push to main triggers Pages deployment.
