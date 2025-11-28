# Graph JSON Schema

The `os-explorer` tool exports the discovered resource graph in a JSON format. This document describes the schema of that JSON output.

## Root Object

| Field | Type | Description |
|---|---|---|
| `project_id` | string | The OpenStack project ID. |
| `project_name` | string | The OpenStack project name. |
| `generated_at` | string (ISO8601) | Timestamp when the graph was generated. |
| `nodes` | array | List of [Node](#node-object) objects. |
| `edges` | array | List of [Edge](#edge-object) objects. |

## Node Object

Represents a resource in the OpenStack project.

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique identifier for the node. Usually the OpenStack UUID, sometimes prefixed (e.g., `volume:uuid` if needed to avoid collisions, though UUIDs are generally unique). |
| `type` | string | Resource type (e.g., `server`, `volume`, `network`, `port`, `load_balancer`). |
| `name` | string | Human-readable name of the resource. |
| `label` | string | Short label for UI display. |
| `meta` | object | Raw metadata from the OpenStack API (sanitized). |
| `created_at` | string | Creation timestamp (if available). |
| `updated_at` | string | Last update timestamp (if available). |
| `partial` | boolean | `true` if data is incomplete due to errors or permissions. |

### Common Node Types

- `server`
- `volume`
- `snapshot`
- `network`
- `subnet`
- `port`
- `router`
- `load_balancer`
- `listener`
- `pool`
- `member`
- `image`
- `stack`
- `zone`

## Edge Object

Represents a relationship between two nodes.

| Field | Type | Description |
|---|---|---|
| `from` | string | `id` of the source node. |
| `to` | string | `id` of the target node. |
| `type` | string | Type of relationship. |
| `meta` | object | Additional metadata for the edge (e.g., device name for attachments). |

### Common Edge Types

- `attached`: Server -> Volume
- `has_port`: Server -> Port
- `on_network`: Port -> Network (implicit or explicit)
- `has_sg`: Port -> Security Group
- `has_listener`: Load Balancer -> Listener
- `has_pool`: Listener -> Pool
- `has_member`: Pool -> Member
- `stack_resource`: Stack -> Resource

## Example

```json
{
  "project_id": "demo-project-id",
  "project_name": "demo",
  "generated_at": "2023-10-27T10:00:00Z",
  "nodes": [
    {
      "id": "server-1",
      "type": "server",
      "name": "web-01",
      "label": "web-01",
      "meta": {}
    },
    {
      "id": "vol-1",
      "type": "volume",
      "name": "vol-3321",
      "label": "vol-3321",
      "meta": {"size_gb": 20}
    }
  ],
  "edges": [
    {
      "from": "server-1",
      "to": "vol-1",
      "type": "attached",
      "meta": {"device": "/dev/vdb"}
    }
  ]
}
```
