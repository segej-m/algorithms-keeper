import logging
from typing import Any

from gidgethub import routing
from gidgethub.sansio import Event

from algorithms_keeper.api import GitHubAPI

workflow_router = routing.Router()

logger = logging.getLogger(__package__)


@workflow_router.register("workflow", action="requested")
async def approve_workflow_run(
    event: Event, gh: GitHubAPI, *args: Any, **kwargs: Any
) -> None:
    """Approve a workflow run from a first-time contributor."""
    workflow_run = event.data["workflow_run"]

    if workflow_run["event"] == "pull_request":
        logger.info("Approving the workflow: %s", workflow_run["html_url"])
        await gh.post(
            workflow_run["url"] + "/approve", data={}, oauth_token=await gh.access_token
        )
