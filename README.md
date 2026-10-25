# Playwright GitHub Issue Tests

Playwright and pytest tests for creating a temporary GitHub repository, filing
an issue, and checking the repository's issues page.

## Requirements

- Python 3.10 or newer
- A GitHub personal access token with permission to create repositories, create
  issues, and delete repositories

## Setup on Windows

From the project directory, create and activate a virtual environment, then
install the dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install pytest pytest-playwright
python -m playwright install chromium
```

Set the token in the current PowerShell session. Replace the placeholder with
your token; do not commit or share it:

```powershell
$env:GITHUB_ACCESS_TOKEN = "YOUR_GITHUB_TOKEN"
```

Run the tests:

```powershell
python -m pytest -v
```

The API tests create a uniquely named repository on your GitHub account and
delete it when the test session finishes. Use a token for an account where
creating and deleting repositories is acceptable. The page test also requires
Chromium to be installed.
