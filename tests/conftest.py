from collections.abc import Iterator
from uuid import uuid4

import pytest
from creds import GITHUB_ACCESS_TOKEN, GITHUB_REPO, GITHUB_USERNAME
from playwright.sync_api import APIRequestContext, APIResponse, Playwright


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    if not GITHUB_ACCESS_TOKEN:
        raise RuntimeError(
            "Set the GITHUB_ACCESS_TOKEN environment variable before running these tests."
        )

    headers = {
        # We set this header per GitHub guidelines.
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    }
    context = playwright.request.new_context(
        base_url="https://api.github.com/",
        extra_http_headers=headers,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def created_repository(api_context: APIRequestContext) -> Iterator[str]:
    repository_name = f"{GITHUB_REPO}-test-{uuid4().hex[:8]}"
    new_repo = api_context.post("/user/repos", data={"name": repository_name})
    assert new_repo.ok, new_repo.text()
    repository_details = new_repo.json()
    repository_owner = repository_details["owner"]["login"]
    assert repository_owner.casefold() == GITHUB_USERNAME.casefold(), (
        f"Token authenticated as {repository_owner}, expected {GITHUB_USERNAME}."
    )
    repository = repository_details["full_name"]
    yield repository
    deleted_repo = api_context.delete(f"/repos/{repository}")
    assert deleted_repo.ok, deleted_repo.text()


@pytest.fixture(scope="session")
def created_issue(
    api_context: APIRequestContext, created_repository: str
) -> APIResponse:
    issue_data = {
        "title": "[Bug] That failed",
        "body": "When running this, that failed with error.",
    }
    issue = api_context.post(
        f"/repos/{created_repository}/issues",
        data=issue_data,
    )
    assert issue.ok, issue.text()
    return issue