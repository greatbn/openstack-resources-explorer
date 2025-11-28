import os
import openstack
from typing import Optional
from dataclasses import dataclass

@dataclass
class Config:
    cloud_name: str
    region_name: Optional[str] = None
    config_file: Optional[str] = None
    project_id: Optional[str] = None
    debug: bool = False
    
    @property
    def connection(self) -> openstack.connection.Connection:
        kwargs = {}
        if self.config_file:
            kwargs["config_files"] = [self.config_file]
        
        # If project_id is provided, we might need to override the auth parameters
        # However, openstack.connect usually takes project_id as an argument to scope the connection
        # But it depends on how the cloud is configured. 
        # If we want to switch project, we usually pass project_id to connect().
        if self.project_id:
            kwargs["project_id"] = self.project_id

        return openstack.connect(
            cloud=self.cloud_name,
            region_name=self.region_name,
            **kwargs
        )

def load_config(cloud: str, region: Optional[str] = None, config_file: Optional[str] = None, project_id: Optional[str] = None, debug: bool = False) -> Config:
    """Load configuration from arguments and environment."""
    # If cloud is not provided, try to get from env
    if not cloud:
        cloud = os.environ.get("OS_CLOUD")
        
    if not cloud:
        # Fallback or error handling could go here, but for now we expect cloud name
        pass

    return Config(cloud_name=cloud, region_name=region, config_file=config_file, project_id=project_id, debug=debug)
