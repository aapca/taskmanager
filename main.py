from task_manager import TaskManager

def print_menu():
    print("\n--- Task Manager ---\n")
    print("Available commands:")
    print("1. Add a new task")
    print("2. List all tasks")
    print("3. Complete a task")
    print("4. Delete a task")
    print("5. Exit the program")

def main():
    task_manager = TaskManager()
    while True:

        print_menu()

        try:
            choice = input("\nEnter your choice (1-5): ")

            match choice:
                case "1":
                    description = input("Enter the task description: ")
                    task_manager.add_task(description)
                case "2":
                    task_manager.list_tasks()
                case "3":
                    task_id = int(input("Enter the task ID to complete: "))
                    task_manager.complete_task(task_id)
                case "4":
                    task_id = int(input("Enter the task ID to delete: "))
                    task_manager.delete_task(task_id)
                case "5":
                    print("Exiting the program. Goodbye!")
                    break
                case _:
                    print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    main()