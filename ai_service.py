import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_simple_task(description):
    if not client.api_key:
        raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    try:
        prompt = f"""Break down the following complex task into a list of 3 to 5 simple, actionable subtasks.
        
        Task: {description}

Response format:
- Subtask 1
- Subtask 2
- Subtask 3
- etc.

Respond using only the list of subtasks, one per line, starting each line with a hyphen."""

        params = {
            "model": "gpt-5",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that breaks down complex tasks into simple, actionable subtasks."},
                {"role": "user", "content": prompt}],
            "max_completion_tokens": 300,
            "verbosity": "medium",
            "reasoning_effort": "minimal"
        }

        response = client.chat.completions.create(**params)
        content = response.choices[0].message.content.strip()

        subtasks = []
        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)

        return subtasks if subtasks else ["Error: No subtasks generated."]
    except Exception as e:
        return ["Error: creating connection to OpenAI API: " + str(e)]