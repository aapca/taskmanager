import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):

    def test_task_creation(self):
        task = Task(1, "Buy groceries")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Buy groceries")
        self.assertFalse(task.completed)

    def test_task_creation_completed(self):
        task = Task(2, "Write tests", completed=True)
        self.assertTrue(task.completed)

    def test_task_str_incomplete(self):
        task = Task(1, "Buy groceries")
        self.assertEqual(str(task), "[ ] #1: Buy groceries")

    def test_task_str_completed(self):
        task = Task(1, "Buy groceries", completed=True)
        self.assertEqual(str(task), "[✔] #1: Buy groceries")


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        # Use a temporary file so tests don't touch the real tasks.json
        self.tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.json', delete=False
        )
        self.tmp.write('[]')
        self.tmp.close()
        self.original_filename = TaskManager.FILENAME
        TaskManager.FILENAME = self.tmp.name

    def tearDown(self):
        TaskManager.FILENAME = self.original_filename
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def _make_manager(self):
        return TaskManager()

    # --- add_task ---

    def test_add_task_adds_to_list(self):
        mgr = self._make_manager()
        mgr.add_task("Task A")
        self.assertEqual(len(mgr._tasks), 1)
        self.assertEqual(mgr._tasks[0].description, "Task A")

    def test_add_task_increments_id(self):
        mgr = self._make_manager()
        mgr.add_task("First")
        mgr.add_task("Second")
        self.assertEqual(mgr._tasks[0].id, 1)
        self.assertEqual(mgr._tasks[1].id, 2)

    def test_add_task_persists_to_file(self):
        mgr = self._make_manager()
        mgr.add_task("Persistent task")
        with open(TaskManager.FILENAME) as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['description'], "Persistent task")

    # --- list_tasks ---

    def test_list_tasks_empty(self, capsys=None):
        mgr = self._make_manager()
        with patch('builtins.print') as mock_print:
            mgr.list_tasks()
            mock_print.assert_called_once_with("No tasks found.")

    def test_list_tasks_prints_tasks(self):
        mgr = self._make_manager()
        mgr.add_task("Task X")
        with patch('builtins.print') as mock_print:
            mgr.list_tasks()
            mock_print.assert_called_once()

    # --- complete_task ---

    def test_complete_task_marks_completed(self):
        mgr = self._make_manager()
        mgr.add_task("Do something")
        mgr.complete_task(1)
        self.assertTrue(mgr._tasks[0].completed)

    def test_complete_task_not_found(self):
        mgr = self._make_manager()
        with patch('builtins.print') as mock_print:
            mgr.complete_task(99)
            mock_print.assert_called_once_with("Task with ID 99 not found.")

    # --- delete_task ---

    def test_delete_task_removes_from_list(self):
        mgr = self._make_manager()
        mgr.add_task("To delete")
        mgr.delete_task(1)
        self.assertEqual(len(mgr._tasks), 0)

    def test_delete_task_not_found(self):
        mgr = self._make_manager()
        with patch('builtins.print') as mock_print:
            mgr.delete_task(99)
            mock_print.assert_called_once_with("Task with ID 99 not found.")

    def test_delete_task_does_not_remove_others(self):
        mgr = self._make_manager()
        mgr.add_task("Keep me")
        mgr.add_task("Delete me")
        mgr.delete_task(2)
        self.assertEqual(len(mgr._tasks), 1)
        self.assertEqual(mgr._tasks[0].description, "Keep me")

    # --- load_tasks ---

    def test_load_tasks_missing_file(self):
        non_existent = self.tmp.name + ".missing.json"
        TaskManager.FILENAME = non_existent
        mgr = TaskManager()
        self.assertEqual(mgr._tasks, [])

    def test_load_tasks_restores_state(self):
        mgr = self._make_manager()
        mgr.add_task("Restored task")
        # Re-instantiate to trigger load
        mgr2 = self._make_manager()
        self.assertEqual(len(mgr2._tasks), 1)
        self.assertEqual(mgr2._tasks[0].description, "Restored task")

    def test_load_tasks_sets_next_id_correctly(self):
        mgr = self._make_manager()
        mgr.add_task("A")
        mgr.add_task("B")
        mgr2 = self._make_manager()
        self.assertEqual(mgr2._next_id, 3)


class TestAiService(unittest.TestCase):

    @patch('ai_service.client')
    def test_create_simple_task_returns_subtasks(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "- Step one\n- Step two\n- Step three"
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "fake-key"

        from ai_service import create_simple_task
        result = create_simple_task("Plan a birthday party")
        self.assertEqual(result, ["Step one", "Step two", "Step three"])

    @patch('ai_service.client')
    def test_create_simple_task_api_error(self, mock_client):
        mock_client.api_key = "fake-key"
        mock_client.chat.completions.create.side_effect = Exception("connection refused")

        from ai_service import create_simple_task
        result = create_simple_task("Some task")
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].startswith("Error:"))

    @patch('ai_service.client')
    def test_create_simple_task_no_subtasks_in_response(self, mock_client):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Sure, I can help!"  # no bullet lines
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "fake-key"

        from ai_service import create_simple_task
        result = create_simple_task("Vague task")
        self.assertEqual(result, ["Error: No subtasks generated."])


if __name__ == '__main__':
    unittest.main()
