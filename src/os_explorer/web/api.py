from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
import openstack.config
from ..cli import run_discovery
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/clouds", response_model=List[str])
def list_clouds():
    """List available clouds from clouds.yaml."""
    try:
        config = openstack.config.loader.OpenStackConfig()
        clouds = [cloud.name for cloud in config.get_all_clouds()]
        clouds.append("Mock Cloud")
        return clouds
    except Exception as e:
        logger.error(f"Error listing clouds: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/graph")
def get_graph(
    cloud: str = Query(..., description="Cloud name in clouds.yaml"),
    region: Optional[str] = Query(None, description="Region name"),
    project_id: Optional[str] = Query(None, description="Project ID to scope discovery to")
) -> Dict[str, Any]:
    """Run discovery and return the resource graph."""
    try:
        if cloud == "Mock Cloud":
            # Try to load graph.json from current directory
            import json
            import os
            if os.path.exists("graph.json"):
                with open("graph.json", "r") as f:
                    return json.load(f)
            else:
                raise HTTPException(status_code=404, detail="graph.json not found for Mock Cloud")

        # We don't pass config_file here, assuming standard locations or env vars
        # If needed we can add a setting for it.
        graph = run_discovery(cloud, region=region, project_id=project_id)
        return graph
    except Exception as e:
        logger.error(f"Error generating graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))
