from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class HeatDiscovery(DiscoveryBase):
    def list_stacks(self) -> Iterable[Any]:
        self.logger.info("Discovering stacks...")
        return self._safe_list(self.conn.orchestration.stacks, project_id=self.project_id)

    def list_stack_resources(self, stack_name_or_id: str) -> Iterable[Any]:
        self.logger.info(f"Discovering resources for stack {stack_name_or_id}...")
        return self._safe_list(self.conn.orchestration.resources, stack_name_or_id)

    def list_all_stack_resources(self, stacks: Iterable[Any]) -> Iterable[Any]:
        resources = []
        for stack in stacks:
            resources.extend(self.list_stack_resources(stack.id))
        return resources

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        stacks = list(self.list_stacks())
        resources = self.list_all_stack_resources(stacks)
        return {
            "stacks": stacks,
            "stack_resources": resources
        }
