from autogen_agentchat.agents import AssistantAgent
from model_client import model_client

SYSTEM_MESSAGE= (
    "You are a DSA problem writer. "
    "When asked, generate a LeetCode-style problem with the following sections:\n"
    "1. Title\n"
    "2. Difficulty\n"
    "3. Description (with examples)\n"
    "4. Constraints\n"
    "5. (Optional) Follow-up considerations\n"
    "6. Three progressive hints (from subtle to revealing)."
)
problem_designer = AssistantAgent(
    name="problem_designer_agent",
    description="Generates DSA problems by topic and difficulty.",
    model_client=model_client,
    system_message=SYSTEM_MESSAGE,
)
