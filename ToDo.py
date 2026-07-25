import json
import os
from datetime import datetime

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks):
    """Add a new task."""
    title = input("Enter task title: ").strip()
    if not title:
        print("❌ Task title cannot be empty!")
        return

    description = input("Enter task description (optional): ").strip()
    priority = input("Enter priority (high/medium/low) [default: medium]: ").strip().lower()

    if priority not in ["high", "medium", "low"]:
        priority = "medium"

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task '{title}' added successfully!")

def view_tasks(tasks, filter_type="all"):
    """Display tasks based on filter."""
    if not tasks:
        print("📭 No tasks found!")
        return

    # Filter tasks
    if filter_type == "completed":
        filtered = [t for t in tasks if t["completed"]]
        title = "✅ Completed Tasks"
    elif filter_type == "pending":
        filtered = [t for t in tasks if not t["completed"]]
        title = "⏳ Pending Tasks"
    else:
        filtered = tasks
        title = "📋 All Tasks"

    if not filtered:
        print(f"No {filter_type} tasks found!")
        return

    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")

    # Priority colors/symbols
    priority_symbols = {
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢"
    }

    for task in filtered:
        status = "✅" if task["completed"] else "⬜"
        priority_symbol = priority_symbols.get(task["priority"], "🟡")
        
        print(f"\n  [{task['id']}] {status} {task['title']}")
        print(f"       Priority: {priority_symbol} {task['priority'].capitalize()}")
        
        if task["description"]:
            print(f"       Description: {task['description']}")
        
        print(f"       Created: {task['created_at']}")
        print(f"  {'-' * 55}")

    print(f"\n  Total: {len(filtered)} task(s)")
    print(f"{'=' * 60}\n")

def complete_task(tasks):
    """Mark a task as completed."""
    view_tasks(tasks, "pending")
    
    if not any(not t["completed"] for t in tasks):
        return

    try:
        task_id = int(input("Enter task ID to mark as complete: "))
        for task in tasks:
            if task["id"] == task_id:
                if task["completed"]:
                    print("⚠️  Task is already completed!")
                else:
                    task["completed"] = True
                    save_tasks(tasks)
                    print(f"✅ Task '{task['title']}' marked as complete!")
                return
        print("❌ Task not found!")
    except ValueError:
        print("❌ Invalid ID! Please enter a number.")

def delete_task(tasks):
    """Delete a task."""
    view_tasks(tasks)
    
    if not tasks:
        return

    try:
        task_id = int(input("Enter task ID to delete: "))
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                confirm = input(f"Are you sure you want to delete '{task['title']}'? (y/n): ")
                if confirm.lower() == "y":
                    tasks.pop(i)
                    # Re-assign IDs
                    for j, t in enumerate(tasks):
                        t["id"] = j + 1
                    save_tasks(tasks)
                    print("🗑️  Task deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
                return
        print("❌ Task not found!")
    except ValueError:
        print("❌ Invalid ID! Please enter a number.")

def edit_task(tasks):
    """Edit an existing task."""
    view_tasks(tasks)
    
    if not tasks:
        return

    try:
        task_id = int(input("Enter task ID to edit: "))
        for task in tasks:
            if task["id"] == task_id:
                print(f"\nEditing Task: '{task['title']}'")
                print("(Press Enter to keep current value)\n")

                new_title = input(f"New title [{task['title']}]: ").strip()
                new_desc = input(f"New description [{task['description']}]: ").strip()
                new_priority = input(f"New priority (high/medium/low) [{task['priority']}]: ").strip().lower()

                if new_title:
                    task["title"] = new_title
                if new_desc:
                    task["description"] = new_desc
                if new_priority in ["high", "medium", "low"]:
                    task["priority"] = new_priority

                save_tasks(tasks)
                print("✏️  Task updated successfully!")
                return
        print("❌ Task not found!")
    except ValueError:
        print("❌ Invalid ID! Please enter a number.")

def search_tasks(tasks):
    """Search tasks by keyword."""
    keyword = input("Enter search keyword: ").strip().lower()
    if not keyword:
        print("❌ Please enter a keyword!")
        return

    results = [
        t for t in tasks
        if keyword in t["title"].lower() or keyword in t["description"].lower()
    ]

    if results:
        print(f"\n🔍 Found {len(results)} result(s) for '{keyword}':")
        view_tasks(results)
    else:
        print(f"🔍 No tasks found for '{keyword}'")

def show_stats(tasks):
    """Show task statistics."""
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed
    high = sum(1 for t in tasks if t["priority"] == "high" and not t["completed"])

    print(f"\n{'=' * 40}")
    print("       📊 Task Statistics")
    print(f"{'=' * 40}")
    print(f"  📋 Total Tasks    : {total}")
    print(f"  ✅ Completed      : {completed}")
    print(f"  ⏳ Pending        : {pending}")
    print(f"  🔴 High Priority  : {high}")
    if total > 0:
        print(f"  📈 Completion Rate: {(completed/total)*100:.1f}%")
    print(f"{'=' * 40}\n")

def clear_completed(tasks):
    """Remove all completed tasks."""
    completed_count = sum(1 for t in tasks if t["completed"])
    
    if completed_count == 0:
        print("⚠️  No completed tasks to clear!")
        return

    confirm = input(f"Delete all {completed_count} completed task(s)? (y/n): ")
    if confirm.lower() == "y":
        tasks[:] = [t for t in tasks if not t["completed"]]
        for i, t in enumerate(tasks):
            t["id"] = i + 1
        save_tasks(tasks)
        print(f"🗑️  Cleared {completed_count} completed task(s)!")
    else:
        print("❌ Operation cancelled.")

def print_menu():
    """Display the main menu."""
    print(f"\n{'=' * 40}")
    print("       📝 TO-DO APP")
    print(f"{'=' * 40}")
    print("  1. ➕ Add Task")
    print("  2. 📋 View All Tasks")
    print("  3. ⏳ View Pending Tasks")
    print("  4. ✅ View Completed Tasks")
    print("  5. ✔️  Complete a Task")
    print("  6. ✏️  Edit a Task")
    print("  7. 🗑️  Delete a Task")
    print("  8. 🔍 Search Tasks")
    print("  9. 📊 Statistics")
    print(" 10. 🧹 Clear Completed Tasks")
    print("  0. 🚪 Exit")
    print(f"{'=' * 40}")

def main():
    """Main function to run the To-Do app."""
    print("Welcome to the To-Do App! 🎉")
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            view_tasks(tasks, "pending")
        elif choice == "4":
            view_tasks(tasks, "completed")
        elif choice == "5":
            complete_task(tasks)
        elif choice == "6":
            edit_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            search_tasks(tasks)
        elif choice == "9":
            show_stats(tasks)
        elif choice == "10":
            clear_completed(tasks)
        elif choice == "0":
            print("\n👋 Goodbye! Stay productive!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
