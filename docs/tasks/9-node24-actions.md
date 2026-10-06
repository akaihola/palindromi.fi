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
