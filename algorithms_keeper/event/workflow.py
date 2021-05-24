from typing import Any

from gidgethub import routing
from gidgethub.sansio import Event

from algorithms_keeper.api import GitHubAPI

workflow_router = routing.Router()


@workflow_router.register("workflow", action="requested")
async def approve_workflow_run(
    event: Event, gh: GitHubAPI, *args: Any, **kwargs: Any
) -> None:
    """Approve a workflow run from a first-time contributor."""
    workflow_run = event.data["workflow_run"]

    if (
        workflow_run["event"] == "pull_request"
        and workflow_run["conclusion"] == "action_required"
    ):
        await gh.post(
            workflow_run["url"] + "/approve", data={}, oauth_token=await gh.access_token
        )
