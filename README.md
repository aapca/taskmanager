# Task Manager

A command-line task manager written in Python that supports manual task creation and AI-powered task breakdown using the OpenAI API.

## Features

- Add tasks manually with a description
- Break down complex tasks into subtasks automatically using OpenAI (GPT)
- List all current tasks with their completion status
- Mark tasks as completed
- Delete tasks
- Persistent storage via a local `tasks.json` file

## Project Structure

```
TaskManager/
├── main.py            # Entry point and CLI menu
├── task_manager.py    # Task and TaskManager classes
├── ai_service.py      # OpenAI integration for task breakdown
├── tasks.json         # Persistent task storage (auto-generated)
├── test_task_manager.py  # Unit tests
├── requirements.txt   # Python dependencies
└── README.md
```

## Requirements

- Python 3.11+
- An OpenAI API key

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd TaskManager
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

```bash
python main.py
```

You will be presented with an interactive menu:

```
--- Task Manager ---

Available commands:
1. Add a new task
2. Add complex task (AI-powered)
3. List all tasks
4. Complete a task
5. Delete a task
6. Exit the program
```

### Adding a simple task

Choose option `1` and enter a description. The task is saved immediately to `tasks.json`.

### Adding an AI-powered complex task

Choose option `2` and describe a complex goal. The AI will break it down into 3–5 actionable subtasks, each added as an individual task.

## Running Tests

```bash
python -m pytest test_task_manager.py -v
```

The test suite covers:

- `Task` class creation and string formatting
- `TaskManager`: adding, listing, completing, and deleting tasks
- Persistence (save/load from JSON)
- `ai_service`: OpenAI response parsing, error handling, and empty-response fallback (all with mocked API calls)

## Environment Variables

| Variable         | Description                        | Required |
|------------------|------------------------------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT access | Yes      |

## License

MIT
