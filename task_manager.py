import json
class Task:
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✔" if self.completed else " "
        return f"[{status}] #{self.id}: {self.description}"
    
class TaskManager:

    FILENAME = "tasks.json"

    def __init__(self):
        self._tasks = []
        self._next_id = 1
        self.load_tasks()

    def add_task(self, description):
        task = Task(self._next_id, description)
        self._tasks.append(task)
        self._next_id += 1
        print(f"Added task: {task}")
        self.save_tasks()

    def list_tasks(self):
        if not self._tasks:
            print("No tasks found.")
        else:
            for task in self._tasks:
                print(task)

    def complete_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                task.completed = True
                print(f"Completed task: {task}")
                self.save_tasks()
                return
        print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                self._tasks.remove(task)
                print(f"Deleted task: {task}")
                self.save_tasks()
                return
        print(f"Task with ID {task_id} not found.")
    
    def save_tasks(self):
        with open(self.FILENAME, 'w') as file:
            json.dump([task.__dict__ for task in self._tasks], file, indent=4)

    def load_tasks(self):
        try:
            with open(self.FILENAME, 'r') as file:
                data = json.load(file)
                self._tasks = [Task(**item) for item in data]
                if self._tasks:
                    self._next_id = max(task.id for task in self._tasks) + 1
                else:
                    self._next_id = 1
        except FileNotFoundError:
            self._tasks = []