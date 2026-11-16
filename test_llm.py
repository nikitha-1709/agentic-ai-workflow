 
from llm import llm

response = llm.invoke(
    "Explain Agentic AI in three simple sentences."
)

print("\nGemini Response:")
print(response.content)
