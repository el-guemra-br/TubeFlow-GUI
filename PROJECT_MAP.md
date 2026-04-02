# Project Structure Map

```text
TubeFlow-GUI/
|-- TubeFlow-GUI.py          # Backward-compatible launcher (entry point)
|-- setup.ps1                # Setup entry point (delegates to scripts/setup.ps1)
|-- requirements.txt         # Python dependencies
|-- README.md
|-- LICENSE
|-- .gitignore
|-- src/
|   `-- tubeflow_gui/
|       |-- __init__.py
|       `-- app.py           # Main GUI application code
|-- scripts/
|   |-- setup.ps1            # Main setup automation script
|   `-- start.ps1            # Start helper script for local runs
`-- docs/
```

## Quick Commands

- Setup: `./setup.ps1`
- Setup and run: `./setup.ps1 -RunAfterSetup`
- Start app: `./scripts/start.ps1`
