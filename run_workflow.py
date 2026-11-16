
from workflow import agent

# Project idea
project_idea = """
Build an AI-powered smart attendance management system
for colleges using face recognition.
"""

# Initial workflow state
initial_state = {
    "project_idea": project_idea,
    "plan": "",
    "action_result": "",
    "evaluation": "",
    "status": "",
    "revision_count": 0,
    "max_revisions": 2
}

print("\n======================================")
print("       AGENTIC AI PROJECT PLANNER")
print("======================================")

# Execute the workflow
result = agent.invoke(
    initial_state,
    config={"recursion_limit": 15}
)

# Display final project plan
print("\n\n======================================")
print("           FINAL PROJECT PLAN")
print("======================================")

print(result["plan"])

# Display evaluation
print("\n\n======================================")
print("           EVALUATION REPORT")
print("======================================")

print(result["evaluation"])

print("\nFinal Status:", result["status"])
print("Total Revisions:", result["revision_count"])

print("\nWorkflow execution completed!")
