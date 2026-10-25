from playwright.sync_api import APIRequestContext, APIResponse, Page


def test_create_issue(created_issue: APIResponse) -> None:
    issue = created_issue.json()
    assert issue["title"] == "[Bug] That failed"
    assert issue["body"] == "When running this, that failed with error."


def test_issue_page(page: Page, created_repository: str) -> None:
    page.goto(f"https://github.com/{created_repository}/issues")
    page.screenshot(path="issues-page.jpg", full_page=True)


def test_new_issue_created(
    api_context: APIRequestContext,
    created_repository: str,
    created_issue: APIResponse,
) -> None:
    all_issues = api_context.get(
        f"/repos/{created_repository}/issues?state=all",
    )

    assert all_issues.ok, all_issues.text()

    expected_issue = created_issue.json()
    new_issue = next(
        (
            issue
            for issue in all_issues.json()
            if issue["number"] == expected_issue["number"]
        ),
        None,
    )

    assert new_issue is not None, "The created issue was not found in the repository."
    assert new_issue["body"] == "When running this, that failed with error."