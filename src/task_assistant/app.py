import streamlit as st
import base64
import uuid

from departments import get_departments
from prompts import get_summary_prompt, get_system_prompt
from call_model import query_model
from firestore_util import write_to_firestore, upload_summary_file


if "messages" not in st.session_state:
    st.session_state.messages = [get_system_prompt()]

if "page" not in st.session_state:
    st.session_state.page = "form"

if "task" not in st.session_state:
    st.session_state.task = {}

if "summary" not in st.session_state:
    st.session_state.summary = None

if "summary_submitted" not in st.session_state:
    st.session_state.summary_submitted = False


def page_form():
    image_path = 'src/task_assistant/image.png'
    encoded_image = base64.b64encode(open(image_path, "rb").read()).decode()

    header_html = f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/jpeg;base64,{encoded_image}" class="header-image" style="width: 50px; height: 50px; border-radius: 20%; border: 2px solid #fff; margin-right: 10px;">
        <h3 style="margin: 10;">Which assistant do you need?</h3>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    with st.form("task_form", clear_on_submit=False):
        department = st.selectbox("Which department do you belong to?", ["" ] + get_departments())
        role = st.text_input("What is your role?")
        pain = st.text_input("What is the biggest pain point in your daily routine (if any, time consuming, annoying, error prone,..)?")
        frequency = st.selectbox("How often do you execute this task?", ["Daily", "Weekly", "Monthly", "One-time"])
        needed_info = st.text_area("Which data or information is needed to perform this specific task (Confluence, E-Mails, Documents,...)")
        submitted = st.form_submit_button("Start Interview")

    if submitted:
        task = {"department": department, "role": role, "pain_point": pain, "task_frequency": frequency, "needed_info": needed_info}
        st.session_state.task = task
        st.session_state.messages.append({"role": "user", "content": f"You have the following information from the employee you are going to interview: : {str(task)}"})
        initial_question = query_model(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": initial_question})
        st.session_state.page = "interview"
        st.experimental_rerun()

        
def page_interview():
    
    container = st.container(border=True)
    container2 = st.container()

    for message in st.session_state.messages[2:]:
        if message["role"] != "system":
            avatar = "🦖" if message["role"] == "user" else "🤖"
            with container:
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

    # Chat input for the user to add new messages
    with container2:
        _, col3 = st.columns([5, 1])
        with col3:
            if st.button("Summarize"):
                st.session_state.page = "summary"
                st.experimental_rerun()
    prompt = st.chat_input("Your message")

    if prompt:
        with container:
            with st.chat_message("user", avatar="🦖"):
                st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Dummy function to simulate model response
        response = query_model(st.session_state.messages)
        with container:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    

def page_summary():
    st.title("Your Summary")

    summary_prompt = get_summary_prompt()
    summary_prompt = summary_prompt + st.session_state.task["needed_info"]
    
    if st.session_state.summary is None:
        st.session_state.messages.append({"role": "user", "content": summary_prompt})
        summary = query_model(st.session_state.messages)
        st.session_state.summary = summary

    st.markdown(st.session_state.summary)

    if st.button("Submit Summary", disabled=st.session_state.summary_submitted):

        uuid1 = uuid.uuid1()
        data = {**st.session_state.task, **{"summary": st.session_state.summary, "id": str(uuid1)}}
        
        public_url = upload_summary_file(data)
        write_to_firestore(data, public_url)
        
        st.session_state.summary_submitted = True
        st.experimental_rerun()
    

def main():
    if st.session_state.page == "form":
        page_form()
    elif st.session_state.page == "interview":
        page_interview()
    elif st.session_state.page == "summary":
        page_summary()


if __name__ == "__main__":
    main()
