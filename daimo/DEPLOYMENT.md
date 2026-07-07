# DAIMO Deployment Runbook

This is the step-by-step procedure for taking DAIMO from its current
local state to a fully FAIR-published ontology.

**Nothing in this runbook has been executed automatically.** Every
step below requires your GitHub and Zenodo credentials and your
explicit action.

Estimated total: **about 90 minutes** plus a 24 – 48 h wait for the
w3id.org PR to be merged.

---

## Before you start

Collect the following, they appear as placeholders throughout:

| Placeholder | What to use | Example |
|---|---|---|
| `<GITHUB_OWNER>` | Your GitHub username or org name | `yayu-liu` or `daimo-ontology` |
| `<REPO_NAME>` | The repo name | `daimo` |
| `<ORCID>` | Your ORCID iD | `0000-0002-1234-5678` |

---

## Step 1 — Push the repo to GitHub (10 min)

```bash
cd /home/yayu/Yayu/PhD/Projects/Papers/daimo

git init
git add .
# Verify .venv, widoco.jar, and __pycache__ are excluded:
cat .gitignore

git commit -m "Initial public release of DAIMO v0.1.6"

# Create an empty repo on GitHub called 'daimo' under your account
# (https://github.com/new). Do NOT initialise it with README/LICENSE —
# we have those locally.

git remote add origin git@github.com:<GITHUB_OWNER>/<REPO_NAME>.git
git branch -M main
git push -u origin main
```

### Tag the release

```bash
git tag -a v0.1.6 -m "DAIMO v0.1.6 — first fully-validated public release candidate"
git push origin v0.1.6
```

---

## Step 2 — Enable GitHub Pages (2 min)

On `https://github.com/<GITHUB_OWNER>/<REPO_NAME>/settings/pages`:

- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/docs`

Save. Within a minute the site is live at:

```
https://<GITHUB_OWNER>.github.io/<REPO_NAME>/
```

Verify the WIDOCO docs load (open `index-en.html`). Verify the WebVOWL
badge resolves the class graph (this requires the site to be served
over HTTPS, which GitHub Pages does by default).

---

## Step 3 — Replace placeholders in the local files (5 min)

Edit these five files and replace every `<GITHUB_OWNER>` / `<REPO_NAME>` /
ORCID placeholder:

| File | Placeholders |
|---|---|
| `CITATION.cff` | `<GITHUB_OWNER>`, author ORCIDs |
| `.zenodo.json` | author ORCIDs if wanted |
| `w3id-redirect/.htaccess` | `<GITHUB_OWNER>` (appears ~14 times) |
| `ontology/daimo-core.ttl` | ORCID placeholders in `dct:creator` (currently dummy IRIs or empty) |
| `README.md` | any remaining placeholders |

Re-run `validate.py` to confirm nothing breaks, then:

```bash
git commit -am "Replace deployment placeholders with concrete account names"
git push
```

---

## Step 4 — Register the w3id.org redirect (15 min + wait)

1. Fork `https://github.com/perma-id/w3id.org`.
2. Copy `w3id-redirect/.htaccess` from this repo to
   `pionera/.htaccess` in your fork. If the directory does not exist,
   create it.
3. Commit with message: *"Add /pionera/ redirect for DAIMO ontology"*.
4. Open a pull request against `perma-id/w3id.org:master`. Use this
   PR description template:

```
/pionera/ — DAIMO ontology maintained by <GITHUB_OWNER>

Namespace : https://w3id.org/pionera/daimo
Redirect target : https://<GITHUB_OWNER>.github.io/<REPO_NAME>/
Ontology license : CC-BY 4.0
Contact : <your-email>

Justification : The /pionera/ path is requested for a small family of
research ontologies produced under the PIONERA programme. DAIMO is
the first ontology in this family; future siblings will share the
prefix. The redirect uses content negotiation (Turtle, RDF/XML,
JSON-LD, N-Triples, HTML).
```

Merge is typically within 24–48 hours. Confirm resolution:

```bash
curl -I https://w3id.org/pionera/daimo
curl -I -H "Accept: text/turtle" https://w3id.org/pionera/daimo
```

Both should return `HTTP/1.1 303 See Other` pointing at your GitHub
Pages URLs.

---

## Step 5 — Zenodo archival and DOI (10 min)

1. Sign in at `https://zenodo.org` with your ORCID or GitHub account.
2. Go to `https://zenodo.org/account/settings/github/`. Enable the
   toggle for `<GITHUB_OWNER>/<REPO_NAME>`.
3. On GitHub, create a new Release from the tag `v0.1.6`:
   `https://github.com/<GITHUB_OWNER>/<REPO_NAME>/releases/new?tag=v0.1.6`
   - Title: *"DAIMO v0.1.6 — first fully-validated public release candidate"*
   - Description: paste the `## [0.1.6]` section from `CHANGELOG.md`.
   - Publish release.
4. Zenodo auto-deposits within a minute. Open the deposit, confirm the
   metadata (pulled from `.zenodo.json`), and publish.
5. Zenodo returns a **concept DOI** (same across all versions) and a
   **versioned DOI** (specific to v0.1.6). Paste the versioned DOI into:
   - `CITATION.cff` → `identifiers[0].value`
   - `README.md` — add a "DOI badge" at the top using
     `https://zenodo.org/badge/DOI/<DOI>.svg`
6. Commit and push the DOI updates; do **not** tag a new release for
   this (Zenodo auto-creates a new deposit for every tag).

---

## Step 6 — Final post-deployment verification (5 min)

All of these must work:

| Check | Command | Expected |
|---|---|---|
| w3id resolves HTML | `curl -sI -L https://w3id.org/pionera/daimo \| head` | chain ending in 200 OK on the GitHub Pages URL |
| w3id resolves Turtle | `curl -sI -L -H "Accept: text/turtle" https://w3id.org/pionera/daimo \| head` | ends on `ontology.ttl`, Content-Type text/turtle |
| w3id resolves RDF/XML | `curl -sI -L -H "Accept: application/rdf+xml" https://w3id.org/pionera/daimo \| head` | ends on `ontology.owl` |
| w3id resolves JSON-LD | `curl -sI -L -H "Accept: application/ld+json" https://w3id.org/pionera/daimo \| head` | ends on `ontology.jsonld` |
| Term IRI | Browser: `https://w3id.org/pionera/daimo#AIAssetOffering` | HTML page scrolls to the class |
| Zenodo DOI | Browser: `https://doi.org/<YOUR-VERSIONED-DOI>` | Zenodo landing page |

When all six pass, **Criterion C10 (FAIR publication) is fully satisfied**.

---

## Step 7 — Advertise (optional, same day)

- Add DAIMO to the Linked Open Vocabularies directory:
  `https://lov.linkeddata.es/dataset/lov/suggest`
- Post a short announcement to the
  [semantic-web@w3.org mailing list](https://lists.w3.org/Archives/Public/semantic-web/)
  with the w3id URL and the Zenodo DOI.
- Add the ontology to the MLDCAT-AP community tracker
  (`https://github.com/SEMICeu/MLDCAT-AP/issues`) if the alignment with
  MLDCAT-AP 3.0.0 is likely to interest that community.

---

## What this runbook does NOT cover

- The **paper rewrite** from Spanish to English. That remains a
  separate workstream (see `../daimo-rewrite-template.md`).
- **Expert interviews** (LOT Phase 1 validation, SWJ criterion C9).
  That is a calendar-scheduling task, not a deployment task.
- **Chowlk class-diagram figure** for paper submission.

Those three blockers remain even after the above steps are done. The
ontology artefact itself, however, will be fully FAIR after Step 6.
