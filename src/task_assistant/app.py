import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import base64

from departments import get_departments

load_dotenv()
client = OpenAI()

dev = False

if "messages" not in st.session_state:
    st.session_state.messages = [
            {"role": "system", "content": """Act as an expert interviewer. You help employess of an organization to identify tedious tasks and reflect on them. Ask questions to help employees to
better understand what specific aspects of the task are painful or tedious. Ask one question at a time!"""},
        ]

if "page" not in st.session_state:
    st.session_state.page = "form"
    if dev:
        st.session_state.messages.append({"role": "assistant", "content": "What specific information is needed to perform the task?"})
        st.session_state.page = "interview"

if "task" not in st.session_state:
    st.session_state.task = {}
    if dev:
        st.session_state.task = {
            "department": "Employee Service",
            "role": "Head of Department",
            "pain": "I need to write lots of emails to answer questions",
            "category": "Answering Questions",
            "frequency": "Weekly",
            "needed_info": "Confluence pages"
        }


def query_model(): 
    #st.write(st.session_state.messages)
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=st.session_state.messages
    )
    return response.choices[0].message.content


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
        initial_question = query_model()
        st.session_state.messages.append({"role": "assistant", "content": initial_question})
        st.session_state.page = "interview"
        st.experimental_rerun()

        
def page_interview():
    for message in st.session_state.messages[2:]:
        if message["role"] != "system":
            if message["role"] == "user":
               avatar = "🦖"
            else:
                avatar = "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("Your message"):
        with st.chat_message("user", avatar="🦖"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        response = query_model()
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.button("Summarize"):
        st.session_state.page = "summary"
        st.experimental_rerun()

def page_summary():
    st.title("Your Summary")

    summary_prompt = """Create a detailed summary in markdown format based on the conducted interview with the following information:
### Summary
Short summary of the task and the interview
### Department and Role
### Task-categories (i.e. Text Summarization, Question Answering,...)
### How AI could help?
Suggest specific tools or techniques based on the following list if if makes sense:

**Tutorials**
- [GPT-2 in 60 lines of Numpy code](https://jaykmody.com/blog/gpt-from-scratch/)
- [An intuition for Attention](https://jaykmody.com/blog/attention-intuition/)

**NLP**
- [NLP with Deep Learning](https://www.youtube.com/watch?v=rmVRLeJRkl4&list=PLoROMvodv4rOSH4v6133s9LFPRHjEmbmJ) Stanford course, Winter 21, Youtube

**RLHF**
- [Reinforcement Learning from Human Feedback: Progress and Challenges](https://www.youtube.com/watch?v=hhiLw5Q_UFg) (John Schulman, Youtube, 2023)
- [Reinforcement Learning from Human Feedback: A Tutorial](https://icml.cc/virtual/2023/tutorial/21554?utm_source=substack&utm_medium=email) (ICML Tutorial, 2023)

**Google GenAI Basics**
1. [Introduction to Large Language Models](https://www.cloudskillsboost.google/course_templates/539)
2. [Introduction to Generative AI](https://www.cloudskillsboost.google/course_templates/536) An introductory course explaining the nature, uses, and differences of Generative AI from traditional machine learning methods.
3. [Introduction to Responsible AI](https://www.cloudskillsboost.google/course_templates/554)Learn what Responsible AI is, why it’s essential, and how Google implements it in its products.
4. [Encoder-Decoder Architecture](https://www.cloudskillsboost.google/course_templates/543) Learn about the encoder-decoder architecture, a critical component of machine learning for sequence-to-sequence tasks.
5. [Introduction to Image Generation](https://www.cloudskillsboost.google/course_templates/541)This course introduces diffusion models, a promising family of machine learning models in the image generation space.
6. [Transformer Models and BERT Model](https://www.cloudskillsboost.google/course_templates/538)A comprehensive introduction to the Transformer architecture and the Bidirectional Encoder Representations from the Transformers (BERT) model.
7. [Attention Mechanism](https://www.cloudskillsboost.google/course_templates/537)This course introduces the attention mechanism, which allows neural networks to focus on specific parts of an input sequence.
8. [Introduction to Generative AI Studio](https://www.cloudskillsboost.google/course_templates/552)This course introduces Generative AI Studio, a product of Vertex AI, guiding users on how to prototype and customize generative AI models.
9. [Create Image Captioning Models](https://www.cloudskillsboost.google/course_templates/542) Learn how to create an image captioning model using deep learning techniques.

**Prompting:**
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/introduction/examples)

**Tools**
- [There is an AI for that](https://theresanaiforthat.com/ai/tutorai/)
"""
    summary_prompt = summary_prompt + st.session_state.task["needed_info"]
    st.session_state.messages.append({"role": "user", "content": summary_prompt})
    summary = query_model()
    st.markdown(summary)

def main():
    if st.session_state.page == "form":
        page_form()
    elif st.session_state.page == "interview":
        page_interview()
    elif st.session_state.page == "summary":
        page_summary()


if __name__ == "__main__":
    main()
