**This approach:**

- Creates a virtual environment in the .venv directory
- Installs all requirements into that environment
- Creates a wrapper script attack-range.sh that automatically activates the virtual environment before running the Python script
- Makes the wrapper script executable

  use ./attack-range.sh instead of directly calling the Python script ./attack-range.py.
