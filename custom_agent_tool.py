from autogen_agentchat.tools import AgentTool

class SafeAgentTool(AgentTool):
    def return_value_as_string(self, value):
        if isinstance(value, str):
            return value
        return super().return_value_as_string(value)

