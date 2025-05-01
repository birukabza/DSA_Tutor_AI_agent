import asyncio
from autogen_agentchat.agents import AssistantAgent
from custom_agent_tool import SafeAgentTool
from autogen_agentchat.ui import Console
from model_client import model_client
from agents.code_analyzer import code_analyzer, docker_executor
from agents.course_teacher import course_teacher
from agents.solution import solution
from function_tools import find_similar_problems_tool,check_problem_exists_tool, generate_and_store_tool


def read_user_input():
    first = input("You: ")
    if first.strip().startswith("```"):
        fence = first.strip()
        lines = [first]
        while True:
            line = input()
            lines.append(line)
            if line.strip() == fence:
                break
        return "\n".join(lines)
    else:
        return first


    
async def main() -> None:
    await docker_executor.start()
    code_analyzer_tool = SafeAgentTool(agent=code_analyzer)
    solution_tool = SafeAgentTool(agent=solution)
    course_teacher_tool = SafeAgentTool(agent=course_teacher)


    user_assistant = AssistantAgent(
    name="assistant_agent",
    model_client=model_client,
    tools=[
        code_analyzer_tool, 
        solution_tool, 
        course_teacher_tool,
        find_similar_problems_tool,
        check_problem_exists_tool,
        generate_and_store_tool,
    ],
    reflect_on_tool_use=True,
    system_message="""
            You are a friendly DSA tutor.

            - To **generate** a new DSA problem, call the `generate_and_store_tool` tool with:
                difficulty: <easy|medium|hard>; topic: <topic>
            - To **check** a submitted solution and get feedback, call the `code_analyzer` tool with both the problem and the user's code in the strictly following the below format:

                
                    ```text
                    task: {
                    "problem": "<full problem statement>",
                    "code": ```python
                    }
                    
                
            - Any Python code should be run by the code analyzer tool and must be given the full problem statement
            
            - To **provide a full solution** for a problem, call `solution_tool` with:
                ```text
                <full problem statement>
                ```
                
            - To provide an explanation on DSA topics call `course_teacher_tool` with:
                <Topics>
                
            - To find **similar problems** the user has worked on before, use the `find_similar_problems` tool with the problem text or topic description.
            
            - …  
                - To find if the user has seen a problem before, call `check_problem_exists_tool` with the full problem text.
                - **After** receiving `true` or `false`, respond with:
                    - If true: “✅ It looks like you’ve already worked on that problem before. Would you like to review it or see related problems?”
                    - If false: “❌ I don’t see that problem in your archive. Shall I generate something new or find similar ones you’ve done?”
                …

            
            - For any other questions or conversation, respond directly without invoking a tool.

            - When giving problem statements to tools it should be full with examples, constraints, hints and everything in it.
            
            - Understand the context and if the user just gives you a code may be the problem is given before, if the user says give me the answer may be the problem is already given by you. Don't ever call the code analyzer tool and solution without a problem statement.
            """
    )


    print("Welcome! Ask me to generate a DSA problem or anything else. Type exit or quit to stop the program.")

    while True:
        try:
            user_input = read_user_input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input or user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        await Console(user_assistant.run_stream(task=user_input)) 
        
    await docker_executor.stop()
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
