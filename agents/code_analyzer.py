
from autogen_agentchat.agents import CodeExecutorAgent
from model_client import model_client
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

SYSTEM_MESSAGE = """
You are a  CommandLineCdeExecutor code executor and analyzer.

When invoked you will receive a single TextMessage whose content includes **two** clearly separated parts:

1) A full problem statement
2) A Python code snippet wrapped in triple backticks, intended to solve that problem.

Your responsibilities:
Before everything make sure the user's code is executed no matter what
1. **Extract** the problem text and the code snippet.  
2. **Execute** the snippet inside the folder `executed_codes`, enforcing time & resource limits via the CancellationToken.  
3. **Capture** the exit code, stdout, and stderr.  
4. **Parse** at least one example from the problem (e.g. `[1,2,3,1]` → `2`).  
5. **Compare** the actual stdout to the expected output:
   - If exit code ≠ 0 or timeout, return **only** stderr or the timeout message.
   - Otherwise, for each example:
     - If stdout exactly matches expected, reply “✅ Correct output for example.”
     - Else reply “❌ For input `[…]` you printed `{actual}`, expected `{expected}`. Hint: <one concrete hint>”
"""

docker_executor = LocalCommandLineCodeExecutor(work_dir="executed_codes")



code_analyzer = CodeExecutorAgent(
    name="code_analyzer",
    code_executor=docker_executor,
    model_client=model_client,
    system_message=SYSTEM_MESSAGE,
)
