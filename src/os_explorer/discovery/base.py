import logging
import openstack
from typing import Dict, Iterable, Any, List
from abc import ABC

class DiscoveryBase(ABC):
    def __init__(self, conn: openstack.connection.Connection, project_id: str, logger: logging.Logger):
        self.conn = conn
        self.project_id = project_id
        self.logger = logger

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        """
        Return per-service iterables/dicts. 
        Must not raise on missing service, returns empty list instead.
        """
        return {}

    def _safe_list(self, list_func, *args, **kwargs) -> Iterable[Any]:
        """Helper to safely list resources, handling missing services or permissions."""
        try:
            return list_func(*args, **kwargs)
        except (openstack.exceptions.EndpointNotFound, openstack.exceptions.ServiceDiscoveryException):
            self.logger.warning(f"Service unavailable for {list_func.__name__}")
            return []
        except openstack.exceptions.ForbiddenException:
            self.logger.warning(f"Permission denied for {list_func.__name__}")
            return []
        except Exception as e:
            self.logger.error(f"Error in {list_func.__name__}: {e}")
            return []
