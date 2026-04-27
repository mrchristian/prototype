# BIM Prototype 02 Quarto Website

This project is configured as a Quarto website and ready for deployment to GitHub Pages using GitHub Actions.

## Site structure

- `index.qmd`: Homepage.
- `project-log.qmd`: Implementation log.
- `wikidata.qmd`: Wikidata notes and references.
- `wikidata-item.ipynb`: Notebook-backed profile page rendered by Quarto.
- `wikidata_profile.py`: Shared Python helper logic used by the notebook page.
- `_quarto.yml`: Quarto project and navigation configuration.

## GitHub Codespace

The repository includes a Dev Container configuration so you can work entirely in the browser without installing anything locally.

1. On the repository page on GitHub, click **Code** → **Codespaces** → **Create codespace on main**.
2. Wait for the container to build — Quarto and Python packages from `requirements.txt` are installed automatically.
3. Once the Codespace is ready, open the integrated terminal and run the Quarto preview server:

```bash
quarto preview
```

4. VS Code will prompt you to open the forwarded port in a browser — click **Open in Browser** to see the live site.
5. To profile a different Wikidata item, open `wikidata-item.ipynb`, update `item_id` in Cell 3, then run all cells or re-run `quarto render`.

## Local development

### One-time local setup

Use one of the setup scripts to create `.venv`, install notebook dependencies, register the local Jupyter kernel, and install Quarto when a supported package manager is available.

Windows (PowerShell):

```powershell
./scripts/setup-local.ps1
```

macOS/Linux:

```bash
chmod +x ./scripts/setup-local.sh
./scripts/setup-local.sh
```

If automatic Quarto installation is not possible on your system, install it from https://quarto.org/docs/get-started/ and then re-run the setup script.

### Run locally

```powershell
quarto preview
```

To render once:

```powershell
quarto render
```

## Update the Wikidata item page

1. Open `wikidata-item.ipynb`.
2. In Cell 3, change `item_id` to the target Wikidata Q-id.
3. Run the notebook cells (or run `quarto render`).
4. Confirm output in `docs/wikidata-item.html`.

The notebook runs a SPARQL query against the Wikidata Query Service, then renders a styled HTML profile with statement cards and summary charts.

## Publish to GitHub Pages

1. Create a GitHub repository and push this folder to the `main` branch.
2. In GitHub, open Settings -> Pages.
3. Under Build and deployment, set Source to **GitHub Actions**.
4. Push changes to `main`.
5. The workflow at `.github/workflows/publish.yml` builds and deploys the `docs` folder.

## Manual deploy from GitHub UI

The workflow supports manual runs via `workflow_dispatch`.

1. Open the repository on GitHub.
2. Go to **Actions** -> **Publish Quarto Site**.
3. Click **Run workflow**.
4. Select the `main` branch and start the run.

## Troubleshooting

- If the notebook fetch fails from Wikidata, re-run `quarto render` after a short delay (the service can rate limit).
- If notebook imports fail after code changes in `wikidata_profile.py`, restart the kernel and run notebook cells again.

## First-time git setup (if needed)

```powershell
git init
git add .
git commit -m "Initialize Quarto website project"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Licence

Code: [![MIT Licence](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENCE)

Content: [![CC BY-SA 4.0](https://img.shields.io/badge/licence-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

Source code is released under the [MIT Licence](LICENCE). Written content, documentation, and non-code assets are licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
