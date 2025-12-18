import streamlit as st
import asyncio
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Import your agent functions
from src.agent.planner import create_planner, plan_question
from src.agent.executor import create_executor, execute
from src.agent.verifier import create_verifier, verify
from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Page config
st.set_page_config(page_title="Reasoning Agent", layout="centered")

# Title
st.title("Reasoning Agent")
st.write("Ask a question and get step-by-step reasoning")

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Process with agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Run the agent
                planner = create_planner(llm)
                executor = create_executor(llm)
                verifier = create_verifier(llm)
                
                plan = asyncio.run(plan_question(planner, prompt))
                exec_out = asyncio.run(execute(executor, prompt, plan))
                verify_out = asyncio.run(verify(verifier, prompt, exec_out))
                
                # Show final answer
                if "final_answer" in exec_out:
                    st.success(f"**Answer:** {exec_out['final_answer']}")
                else:
                    st.info("Analysis complete")
                
                # Show details in expander
                with st.expander("View reasoning steps"):
                    st.write("**Planning:**")
                    st.json(plan)
                    st.write("**Execution:**")
                    st.json(exec_out)
                    st.write("**Verification:**")
                    st.json(verify_out)
                
                # Save to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": exec_out.get("final_answer", "Analysis complete")
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Error: {str(e)}"
                })

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()