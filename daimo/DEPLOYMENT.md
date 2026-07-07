# DAIMO Deployment Runbook

This is the step-by-step procedure for taking DAIMO from its current
local state to a fully FAIR-published ontology.

**Repository context (2026-07-08):** DAIMO lives inside the monorepo
`EdmundoMori/Papers-DAIMO` under `daimo/`. GitHub Pages serves
`daimo/docs/` via `.github/workflows/daimo-pages.yml` at
`https://edmundomori.github.io/Papers-DAIMO/`.

**Nothing in this runbook has been executed automatically.** Steps that
require GitHub/Zenodo/w3id credentials need your explicit action.

Estimated total: **about 60 minutes** plus a 24–48 h wait for the
w3id.org PR to be merged.

---

## Before you start

| Placeholder | What to use | Current value |
|---|---|---|
| `<GITHUB_OWNER>` | GitHub username or org | `EdmundoMori` |
| `<REPO_NAME>` | Monorepo name | `Papers-DAIMO` |
| `<RELEASE_TAG>` | Frozen review tag | `v0.1.6-swj-submission` |
| `<ORCID>` | Author ORCID iD | add when available |

---

## Step 1 — Confirm the frozen release tag (5 min)

The tag `v0.1.6-swj-submission` is prepared in the repository. After push,
publish a GitHub Release from it:

```
https://github.com/EdmundoMori/Papers-DAIMO/releases/new?tag=v0.1.6-swj-submission
```

- Title: *DAIMO v0.1.6 — SWJ submission release candidate*
- Description: paste the `## [0.1.6]` section from `CHANGELOG.md`.

---

## Step 2 — Enable GitHub Pages (5 min)

On `https://github.com/EdmundoMori/Papers-DAIMO/settings/pages`:

- **Source**: GitHub Actions
- Run workflow **Deploy DAIMO documentation** (or push to trigger it)

Verify:

```
https://edmundomori.github.io/Papers-DAIMO/index-en.html
```

---

## Step 3 — Register the w3id.org redirect (15 min + wait)

1. Fork `https://github.com/perma-id/w3id.org`.
2. Copy `daimo/w3id-redirect/.htaccess` to `pionera/.htaccess` in your fork.
3. Open a PR against `perma-id/w3id.org:master`.

Confirm after merge:

```bash
curl -I https://w3id.org/pionera/daimo
curl -I -H "Accept: text/turtle" https://w3id.org/pionera/daimo
```

---

## Step 4 — Zenodo archival and DOI (10 min)

1. Sign in at `https://zenodo.org` with ORCID or GitHub.
2. Enable Zenodo for `EdmundoMori/Papers-DAIMO` at
   `https://zenodo.org/account/settings/github/`.
3. Publish the GitHub Release `v0.1.6-swj-submission`.
4. Zenodo auto-deposits; confirm metadata from `daimo/.zenodo.json` and publish.
5. Insert the **versioned DOI** into `daimo/CITATION.cff`, `daimo/README.md`,
   and the Availability section of both paper versions.

---

## Step 5 — Final verification (5 min)

| Check | Expected |
|---|---|
| GitHub release | `v0.1.6-swj-submission` downloadable |
| GitHub Pages | WIDOCO HTML + serialisations resolve |
| w3id HTML | 303 → GitHub Pages |
| w3id Turtle | 303 → `ontology.ttl` |
| Zenodo DOI | Landing page resolves |
| Local replay | `validate.py` + `reasoner_check.py` exit 0 |

When all pass, **Criterion C10 (FAIR publication) is fully satisfied**.

---

## What this runbook does NOT cover

- **Expert interviews** (LOT Phase 1 / SWJ criterion C9) — scheduling task.
- **ORCID registration** — optional; add real IRIs when available.
- **Chowlk class-diagram figure** — separate from FAIR closure.

