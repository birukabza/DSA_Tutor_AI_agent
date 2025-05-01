from db_manager import ProblemDBManager
from autogen_core.tools import FunctionTool
from agents.problem_designer import problem_designer
from typing import List
db_manager = ProblemDBManager()


def find_similar_problems(query_text: str) -> str:
    similar_problems = db_manager.get_similar_problems(query_text)
    if not similar_problems:
        return "No similar problems found."
    lines = ["Similar problems you've worked on before:"]
    for i, p in enumerate(similar_problems, 1):
        lines.append(f"{i}. [{p['difficulty']}] {p['topic']}\n{p['problem']}")
    return "\n\n".join(lines)

def check_problem_exists(problem_text: str) -> bool:
    return db_manager.is_problem_exists(problem_text)

async def generate_and_store(difficulty: str, topic: str) -> str:
    prompt = (
        f"Please generate a new DSA problem.\n"
        f"- Difficulty: {difficulty}\n"
        f"- Topic: {topic}\n\n"
        f"Output should include:\n"
        f"1. Title\n2. Difficulty\n3. Description with examples\n"
        f"4. Constraints\n5. (Optional) Follow-up\n6. Three hints\n"
    )
    def return_value_as_string(value) -> str:
        """Convert the task result to a string."""
        parts: List[str] = []
        for message in value.messages:
            parts.append(f"{message.source}: {message.to_model_text()}")
        return "\n\n".join(parts)

    result = await problem_designer.run(task=prompt)
    problem_text = return_value_as_string(result)

    problem_id = db_manager.add_problem(problem_text, difficulty, topic)

    return (
        f"{problem_text}\n\n"
        f"✅ Problem stored with ID: {problem_id}"
    )


generate_and_store_tool = FunctionTool(
            name="generate_and_store_tool",
            func=generate_and_store,
            description="**Saves the problem to the database with its difficulty and topic after generating the problem"
                )
find_similar_problems_tool = FunctionTool(
    name="find_similar_problems",
    func=find_similar_problems,
    description="Retrieve problems from your database that are similar to a query."
)
check_problem_exists_tool = FunctionTool(
    name="check_problem_exists_tool",
    func=check_problem_exists,
    description="Returns true if the given problem text already exists in your database."
)