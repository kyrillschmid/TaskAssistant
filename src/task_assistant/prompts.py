

def get_system_prompt():

    return {"role": "system", "content": """Act as an expert interviewer. You help employees of an organization to identify tedious tasks and reflect on them. Ask questions to help
better understand what specific aspects of the task are painful or tedious. Ask one question at a time!"""}

def get_summary_prompt():
    return """Create a detailed summary in markdown format based on the conducted interview containing the following information:
### Summary
Give a short summary of the task and the interview

### Department and Role

### Task-categories (i.e. Text Summarization, Question Answering, Information Retrieval, ..)

### How AI could help?
Suggest specific tools or techniques that could be used. Here is a list of common tools and techniques:

Tutorials:
- [GPT-2 in 60 lines of Numpy code](https://jaykmody.com/blog/gpt-from-scratch/)
- [An intuition for Attention](https://jaykmody.com/blog/attention-intuition/)

NLP_
- [NLP with Deep Learning](https://www.youtube.com/watch?v=rmVRLeJRkl4&list=PLoROMvodv4rOSH4v6133s9LFPRHjEmbmJ) Stanford course, Winter 21, Youtube

RLHF:
- [Reinforcement Learning from Human Feedback: Progress and Challenges](https://www.youtube.com/watch?v=hhiLw5Q_UFg) (John Schulman, Youtube, 2023)
- [Reinforcement Learning from Human Feedback: A Tutorial](https://icml.cc/virtual/2023/tutorial/21554?utm_source=substack&utm_medium=email) (ICML Tutorial, 2023)

Google GenAI Basics:
1. [Introduction to Large Language Models](https://www.cloudskillsboost.google/course_templates/539)
2. [Introduction to Generative AI](https://www.cloudskillsboost.google/course_templates/536) An introductory course explaining the nature, uses, and differences of Generative AI from traditional machine learning methods.
3. [Introduction to Responsible AI](https://www.cloudskillsboost.google/course_templates/554)Learn what Responsible AI is, why it’s essential, and how Google implements it in its products.
4. [Encoder-Decoder Architecture](https://www.cloudskillsboost.google/course_templates/543) Learn about the encoder-decoder architecture, a critical component of machine learning for sequence-to-sequence tasks.
5. [Introduction to Image Generation](https://www.cloudskillsboost.google/course_templates/541)This course introduces diffusion models, a promising family of machine learning models in the image generation space.
6. [Transformer Models and BERT Model](https://www.cloudskillsboost.google/course_templates/538)A comprehensive introduction to the Transformer architecture and the Bidirectional Encoder Representations from the Transformers (BERT) model.
7. [Attention Mechanism](https://www.cloudskillsboost.google/course_templates/537)This course introduces the attention mechanism, which allows neural networks to focus on specific parts of an input sequence.
8. [Introduction to Generative AI Studio](https://www.cloudskillsboost.google/course_templates/552)This course introduces Generative AI Studio, a product of Vertex AI, guiding users on how to prototype and customize generative AI models.
9. [Create Image Captioning Models](https://www.cloudskillsboost.google/course_templates/542) Learn how to create an image captioning model using deep learning techniques.

Prompting:
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/introduction/examples)

Tools
- [There is an AI for that](https://theresanaiforthat.com/ai/tutorai/)
"""