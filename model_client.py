from autogen_ext.models.openai import OpenAIChatCompletionClient


model_client = OpenAIChatCompletionClient(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1024,
        timeout=30,
)
