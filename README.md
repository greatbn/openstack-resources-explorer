# OpenStack Resource Viewer

A web-based tool to visualize and explore OpenStack resources.

## Features

- **Resource Tree**: Hierarchical view of resources.
- **Detailed Relations**: View attached volumes, ports, security groups, and more for a selected resource.
- **Mock Mode**: Explore the UI with sample data without a live OpenStack connection.
- **Graph Visualization**: (Optional) Force-directed graph view of resource relationships.

## Prerequisites

- Python 3.8+
- Node.js 16+
- OpenStack credentials (if connecting to a real cloud)

## Backend Setup

1.  **Install Dependencies**:
    ```bash
    pip install -e .
    ```

2.  **Run the API Server**:
    ```bash
    uvicorn src.os_explorer.web.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be available at `http://localhost:8000`.

## Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd web_ui
    ```

2.  **Install Dependencies**:
    ```bash
    npm install
    ```

3.  **Run the Development Server**:
    ```bash
    npm run dev
    ```
    The UI will be available at `http://localhost:5173`.

## Usage

### Web Interface

1.  Open your browser and navigate to `http://localhost:5173`.
2.  **Mock Mode**: Select "Mock Cloud" from the dropdown to load sample data (`graph.json`).
3.  **Real Cloud**: Ensure you have a `clouds.yaml` file configured and select your cloud from the dropdown.

### Command Line Interface (CLI)

The tool also provides a CLI for discovering resources and generating the graph JSON file.

#### Discover Resources

Discover resources from a cloud and save them to a JSON file:

```bash
os-explorer discover --cloud <cloud-name> --out graph.json
```

Options:
- `--cloud`: Name of the cloud in `clouds.yaml` (required).
- `--region`: Region name (optional).
- `--config-file`: Path to `clouds.yaml` (optional).
- `--project-id`: Project ID to scope discovery to (optional).
- `--out`: Output JSON file path (default: `graph.json`).
- `--debug`: Enable debug logging.

#### View Resource Tree

Display a tree view of resources in the terminal:

```bash
os-explorer tree --cloud <cloud-name>
```

Or view a tree from a saved JSON file:

```bash
os-explorer tree --file graph.json
```

Options:
- `--cloud`: Name of the cloud in `clouds.yaml`.
- `--file`: Path to a JSON graph file.
- `--types`: Comma-separated list of resource types to filter (e.g., `server,network`).


## Project Structure

- `src/os_explorer`: Python backend code.
- `web_ui`: React frontend code.
- `graph.json`: Sample data for Mock Mode.
