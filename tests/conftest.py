from collections.abc import Iterator
import os
from uuid import uuid4

import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Playwright


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not token:
        raise RuntimeError(
            "Set the GITHUB_ACCESS_TOKEN environment variable before running these tests."
        )

    headers = {
        # We set this header per GitHub guidelines.
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
    }
    context = playwright.request.new_context(
        base_url="https://api.github.com/",
        extra_http_headers=headers,
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def created_repository(api_context: APIRequestContext) -> Iterator[str]:
    repository_name = f"playwright-issue-test-{uuid4().hex[:8]}"
    new_repo = api_context.post("/user/repos", data={"name": repository_name})
    assert new_repo.ok, new_repo.text()
    repository = new_repo.json()["full_name"]
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