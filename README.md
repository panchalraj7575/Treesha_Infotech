# Task Management API with CLI Interface
A RESTful Task Management system with both an API backend and a command-line interface built with Python.

## Installation
1. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Configure Environment Variables** (recommended)

3. **Run the Setup Script**
   ```bash
   python seed.py
   ```

The API will be available at `http://127.0.0.1:8000/api/tasks/`

### 3. Use the CLI

Open a new terminal window (keep the server running)
### Interactive Menu Mode
```bash
python tasks/cli.py menu
```

This launches an interactive menu with the following options:
1. Create Task
2. List Tasks
3. Get Task
4. Update Task
5. Delete Task
6. Mark as Complete
7. Exit

### Direct Command Mode

#### List tasks
```bash
python tasks/cli.py list --page 1 --limit 10 --ordering id --search "urgent"
```

#### Get a specific task
```bash
python tasks/cli.py get 5
```

#### Add a new task
```bash
python tasks/cli.py add "Complete API testing" HIGH --description "Test all endpoints" --due_date 2026-01-25
```

#### Update a task
```bash
python tasks/cli.py update 5 --title "New title" --priority LOW --status true --due_date 2026-01-28
```

#### Mark task as complete
```bash
python tasks/cli.py complete 5
```

#### Delete a task
```bash
python tasks/cli.py delete 5
```

