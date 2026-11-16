
import streamlit as st
from workflow import agent

# Page configuration
st.set_page_config(
    page_title="AI Project Planner",
    page_icon="🤖",
    layout="wide"
)

# Application heading
st.title("🤖 Agentic AI Project Planner")

st.write(
    "An AI-powered agent that plans, validates, "
    "evaluates, and improves project ideas."
)

st.divider()

# User input
st.subheader("Enter Your Project Idea")

project_idea = st.text_area(
    "Describe the project you want to plan:",
    placeholder="Example: Build an AI-powered smart attendance system...",
    height=150
)

max_revisions = st.slider(
    "Maximum number of revisions",
    min_value=0,
    max_value=3,
    value=2
)

# Generate button
if st.button("Generate Project Plan", type="primary"):

    if not project_idea.strip():
        st.warning("Please enter a project idea first.")

    else:
        initial_state = {
            "project_idea": project_idea,
            "plan": "",
            "action_result": "",
            "evaluation": "",
            "status": "",
            "revision_count": 0,
            "max_revisions": max_revisions
        }

        with st.spinner(
            "AI Agent is planning and evaluating your project..."
        ):
            try:
                result = agent.invoke(
                    initial_state,
                    config={"recursion_limit": 15}
                )

                st.success("Workflow execution completed!")

                st.divider()

                st.subheader("📋 Generated Project Plan")
                st.markdown(result["plan"])

                st.divider()

                st.subheader("🔍 Validation Result")
                st.write(result["action_result"])

                st.subheader("🧠 Evaluation Report")
                st.markdown(result["evaluation"])

                st.divider()

                st.subheader("📊 Workflow Summary")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Final Status",
                        result["status"]
                    )

                with col2:
                    st.metric(
                        "Total Revisions",
                        result["revision_count"]
                    )

                if result["status"] == "APPROVED":
                    st.success("Your project plan has been approved!")

                else:
                    st.warning(
                        "The workflow stopped without approval. "
                        "Review the evaluation report."
                    )

            except Exception as error:
                st.error(f"Workflow error: {error}")

st.divider()

st.caption("Built using Python, Gemini API, LangGraph and Streamlit.")
 