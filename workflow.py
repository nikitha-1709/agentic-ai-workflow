
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from llm import llm


# 1. Define the workflow state
class WorkflowState(TypedDict):
    project_idea: str
    plan: str
    action_result: str
    evaluation: str
    status: str
    revision_count: int
    max_revisions: int


# 2. Planning node
def planning_node(state: WorkflowState):

    print("\n[PLANNING] Generating project plan...")

    prompt = f"""
    You are an AI project planning agent.

    Create a detailed project plan for:
    {state['project_idea']}

    Include these sections:
    1. Project Overview
    2. Objectives
    3. Technology Stack
    4. Tasks and Milestones
    5. Timeline
    6. Resources Required
    7. Expected Deliverables
    8. Potential Risks

    Make the plan realistic, clear and structured.
    """

    response = llm.invoke(prompt)

    return {"plan": response.content}


# 3. Action node
def action_node(state: WorkflowState):

    print("\n[ACTION] Validating the generated plan...")

    required_sections = [
        "Project Overview",
        "Objectives",
        "Technology Stack",
        "Tasks and Milestones",
        "Timeline",
        "Resources Required",
        "Expected Deliverables",
        "Potential Risks"
    ]

    plan = state["plan"].lower()

    missing_sections = [
        section for section in required_sections
        if section.lower() not in plan
    ]

    if missing_sections:
        result = (
            "Validation failed. Missing sections: "
            + ", ".join(missing_sections)
        )
    else:
        result = (
            "Validation successful. All eight required "
            "sections are present."
        )

    print(result)

    return {"action_result": result}


# 4. Evaluation node


 
def evaluation_node(state: WorkflowState):

    print("\n[EVALUATION] Evaluating project plan...")

    prompt = f"""
    You are an AI quality evaluator.

    Evaluate this project plan:

    {state['plan']}

    Validation result:
    {state['action_result']}

    Check:
    - Completeness
    - Clarity
    - Feasibility
    - Realistic timeline
    - Quality of deliverables

    If satisfactory, your FIRST line must be APPROVED.
    If improvements are needed, your FIRST line must be REVISE.

    Explain your decision after the first line.
    """

    response = llm.invoke(prompt)
    evaluation = response.content.strip()

    print("\nEvaluator response:")
    print(evaluation)

    first_line = evaluation.splitlines()[0].strip().upper()

    if first_line.startswith("APPROVED"):
        status = "APPROVED"
    else:
        status = "NEEDS_REVISION"

    print("\nEvaluation status:", status)

    return {
        "evaluation": evaluation,
        "status": status
    }


# 5. Revision node
def revision_node(state: WorkflowState):

    print("\n[REVISION] Improving the project plan...")

    prompt = f"""
    Improve the following project plan.

    Original plan:
    {state['plan']}

    Evaluator feedback:
    {state['evaluation']}

    Validation feedback:
    {state['action_result']}

    Fix the identified weaknesses.
    Preserve all eight required sections.
    Return the complete improved project plan.
    """

    response = llm.invoke(prompt)

    return {
        "plan": response.content,
        "revision_count": state["revision_count"] + 1
    }


# 6. Decide whether to finish or revise

def route_after_evaluation(state: WorkflowState):

    if state["status"] == "APPROVED":
        print("\n[COMPLETE] Project plan approved!")
        return "end"

    if state["revision_count"] >= state["max_revisions"]:
        print("\n[STOP] Maximum revision limit reached.")
        return "end"

    return "revise"
# Build the LangGraph workflow
graph = StateGraph(WorkflowState)

graph.add_node("plan", planning_node)
graph.add_node("action", action_node)
graph.add_node("evaluate", evaluation_node)
graph.add_node("revise", revision_node)

graph.add_edge(START, "plan")
graph.add_edge("plan", "action")
graph.add_edge("action", "evaluate")

graph.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "revise": "revise",
        "end": END
    }
)

graph.add_edge("revise", "action")

# Compile the workflow
agent = graph.compile()

print("\nAgentic AI workflow compiled successfully!")