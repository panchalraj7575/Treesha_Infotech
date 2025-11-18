import typer
import requests
import json

API_URL = "http://127.0.0.1:8000/api/tasks/"

app = typer.Typer()


@app.command()
def get(id: int):
    """Get a single task by ID"""
    response = requests.get(f"{API_URL}{id}/")

    try:
        data = response.json()
        typer.echo(json.dumps(data, indent=4))
    except Exception:
        typer.echo("Invalid response or task not found")


@app.command()
def list(page: int = 1, limit: int = 5, ordering: str = "id", search: str = ""):
    """List tasks with pagination using page + limit (JSON output)."""
    url = f"{API_URL}?page={page}&limit={limit}&ordering={ordering}"

    if search:
        url += f"&search={search}"

    response = requests.get(url)

    try:
        data = response.json()
    except Exception:
        typer.echo("Invalid response from server")
        raise typer.Exit()

    typer.echo(json.dumps(data, indent=4))


@app.command()
def add(
    title: str,
    priority: str,
    description: str = "",
    due_date: str = typer.Option(None, "--due_date"),
):
    """Add a new task"""
    data = {
        "title": title,
        "priority": priority,
        "description": description,
        "due_date": due_date,
    }
    response = requests.post(API_URL, json=data)
    print(response.json())


@app.command()
def update(
    id: int,
    title: str = None,
    description: str = None,
    priority: str = None,
    due_date: str = typer.Option(None, "--due_date", help="Due date YYYY-MM-DD"),
    status: str = typer.Option(None, "--status", help="true or false"),
):
    """Update a task with all fields"""

    data = {}

    if title is not None:
        data["title"] = title

    if description is not None:
        data["description"] = description

    if priority is not None:
        data["priority"] = priority

    if due_date is not None:
        data["due_date"] = due_date

    if status is not None:
        data["status"] = status

    response = requests.patch(f"{API_URL}{id}/", json=data)

    try:
        typer.echo(json.dumps(response.json(), indent=4))
    except:
        typer.echo("Invalid response from server")


@app.command()
def complete(id: int):
    """Mark task as completed"""
    response = requests.patch(f"{API_URL}{id}/", json={"status": True})
    print(response.json())


@app.command()
def delete(id: int):
    """Delete a task"""
    response = requests.delete(f"{API_URL}{id}/")
    print("Deleted" if response.status_code == 204 else "Failed")


@app.command()
def menu():
    """Interactive menu for task management"""
    while True:
        typer.echo("\n---------------------------------")
        typer.echo("        TASK MANAGER MENU        ")
        typer.echo("---------------------------------")
        typer.echo("1. Create Task")
        typer.echo("2. List Tasks")
        typer.echo("3. Get Task")
        typer.echo("4. Update Task")
        typer.echo("5. Delete Task")
        typer.echo("6. Mark as Complete")
        typer.echo("7. Exit")
        typer.echo("---------------------------------\n")

        choice = typer.prompt("Enter your choice (1-7)")

        # 1️⃣ CREATE
        if choice == "1":
            title = typer.prompt("Title")
            priority = typer.prompt("Priority (LOW/MEDIUM/HIGH)")
            description = typer.prompt("Description", default="")
            due_date = typer.prompt("Due Date (YYYY-MM-DD)", default="")
            data = {
                "title": title,
                "priority": priority,
                "description": description,
                "due_date": due_date or None,
            }
            response = requests.post(API_URL, json=data)
            typer.echo(json.dumps(response.json(), indent=4))

        # 2️⃣ LIST
        elif choice == "2":
            page = typer.prompt("Page", default=1)
            limit = typer.prompt("Limit", default=5)
            ordering = typer.prompt("Ordering (id/title/priority)", default="id")
            search = typer.prompt("Search", default="")
            url = f"{API_URL}?page={page}&limit={limit}&ordering={ordering}&search={search}"
            response = requests.get(url)
            typer.echo(json.dumps(response.json(), indent=4))

        # 3️⃣ GET
        elif choice == "3":
            task_id = typer.prompt("Enter Task ID")
            response = requests.get(f"{API_URL}{task_id}/")
            typer.echo(json.dumps(response.json(), indent=4))

        # 4️⃣ UPDATE
        elif choice == "4":
            task_id = typer.prompt("Enter Task ID")
            title = typer.prompt("New title (leave blank to skip)", default="")
            description = typer.prompt(
                "New description (leave blank to skip)", default=""
            )
            priority = typer.prompt("New priority (LOW/MEDIUM/HIGH)", default="")
            due_date = typer.prompt("New due date (YYYY-MM-DD)", default="")
            status = typer.prompt("Status (true/false)", default="")

            data = {}
            if title:
                data["title"] = title
            if description:
                data["description"] = description
            if priority:
                data["priority"] = priority
            if due_date:
                data["due_date"] = due_date
            if status:
                data["status"] = True if status.lower() == "true" else False

            response = requests.patch(f"{API_URL}{task_id}/", json=data)
            typer.echo(json.dumps(response.json(), indent=4))

        # 5️⃣ DELETE
        elif choice == "5":
            task_id = typer.prompt("Enter Task ID")
            response = requests.delete(f"{API_URL}{task_id}/")
            typer.echo("Deleted" if response.status_code == 204 else "Failed")

        # 6️⃣ COMPLETE
        elif choice == "6":
            task_id = typer.prompt("Enter Task ID")
            response = requests.patch(f"{API_URL}{task_id}/", json={"status": True})
            typer.echo(json.dumps(response.json(), indent=4))

        # 7️⃣ EXIT
        elif choice == "7":
            typer.echo("Goodbye!")
            break

        else:
            typer.echo("Invalid choice. Please enter 1–7.")


if __name__ == "__main__":
    app()
