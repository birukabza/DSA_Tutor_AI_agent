from autogen_agentchat.agents import AssistantAgent
from model_client import model_client


SYSTEM_MESSAGE = """
You are a data structure and algorithm teacher. Your task is to give the best explanations to a given topic with real world examples
"""

course_teacher = AssistantAgent(
    name="course_teacher_agent",
    description="",
    model_client=model_client,
    system_message=SYSTEM_MESSAGE
)