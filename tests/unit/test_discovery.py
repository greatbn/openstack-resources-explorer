import sys
from unittest.mock import MagicMock

# Define exceptions that are used in the code
class MockEndpointNotFound(Exception): pass
class MockServiceDiscoveryException(Exception): pass
class MockForbiddenException(Exception): pass

# Mock openstack module before importing os_explorer
mock_openstack = MagicMock()
mock_exceptions = MagicMock()
mock_exceptions.EndpointNotFound = MockEndpointNotFound
mock_exceptions.ServiceDiscoveryException = MockServiceDiscoveryException
mock_exceptions.ForbiddenException = MockForbiddenException

mock_openstack.exceptions = mock_exceptions

sys.modules["openstack"] = mock_openstack
sys.modules["openstack.connection"] = MagicMock()
sys.modules["openstack.exceptions"] = mock_exceptions

import pytest
from os_explorer.discovery.compute import ComputeDiscovery

def test_compute_discovery_list_servers():
    mock_conn = MagicMock()
    mock_server = MagicMock()
    mock_server.id = "s1"
    mock_server.name = "server1"
    mock_conn.compute.servers.return_value = [mock_server]
    mock_conn.compute.servers.__name__ = "list_servers"
    
    cd = ComputeDiscovery(mock_conn, "p1", MagicMock())
    servers = list(cd.list_servers())
    
    assert len(servers) == 1
    assert servers[0].id == "s1"
    mock_conn.compute.servers.assert_called_once()

def test_compute_discovery_error_handling():
    mock_conn = MagicMock()
    # Simulate service unavailable using the mocked exception
    mock_conn.compute.servers.side_effect = MockEndpointNotFound()
    mock_conn.compute.servers.__name__ = "list_servers"
    
    cd = ComputeDiscovery(mock_conn, "p1", MagicMock())
    servers = list(cd.list_servers())
    
    assert len(servers) == 0
