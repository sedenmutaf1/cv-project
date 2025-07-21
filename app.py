# If you come across these codes, you must know that this project is purely educational for me.
# That's why it will have a lot of comment lines to explain everything.

import os  # This is used to load the environment variables from the .env file
from dotenv import load_dotenv  # This is used to load the environment variables from the .env file
from openai import OpenAI  # This is used to interact with the OpenAI API
from pypdf import PdfReader  # This is used to read the PDF file 
import gradio as gr  # This is used to create the Gradio interface


load_dotenv()  # Load environment variables from the .env file
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize OpenAI API
name = "Seden Mutaf"

# This part reads a pdf file and returns the text.
def get_pdf_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# This reads my cover letter and stores it in a variable.
with open("assets/coverletter.txt", "r", encoding="utf-8") as f:
    coverletter = f.read()

linkedin = get_pdf_text("assets/Profile.pdf")
cv = get_pdf_text("assets/cv.pdf")

# This is the system prompt that ensures the chatbot acts like me.
system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, " \
                f"particularly questions related to {name}'s career, background, skills and experience. " \
                f"Your responsibility is to represent {name} for interactions on the website as faithfully as possible. " \
                f"You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. " \
                f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. " \
                f"If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{coverletter}\n\n## LinkedIn Profile:\n{linkedin}\n\n## CV:\n{cv}"
system_prompt += f"\n\nWith this context, please chat with the user, always staying in character as {name}."

# This function handles the conversation logic
def chat(message, history):
    # Convert Gradio-style history to OpenAI-style message list
    formatted_history = []
    for user_msg, assistant_msg in history:
        formatted_history.append({"role": "user", "content": user_msg})
        formatted_history.append({"role": "assistant", "content": assistant_msg})

    messages = [{"role": "system", "content": system_prompt}] + formatted_history + [{"role": "user", "content": message}]
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

# Gradio interface layout
with gr.Blocks(css="""
:root { color-scheme: dark !important; }
body {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
}
.gradio-container {
    max-width: 1500px;
    margin: auto;
    padding: 2rem;
    background-color: #161b22 !important;
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(0,0,0,0.5);
}
.gr-chatbot, .chatbot, .wrap.svelte-1ipelgc, .message.svelte-1ipelgc {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
}
input, textarea {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
}
button {
    background-color: #238636 !important;
    color: white !important;
    border: none !important;
}
button:hover {
    background-color: #2ea043 !important;
}
a {
    color: #58a6ff !important;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
""") as demo:

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image("assets/profile.jpg", 
                     label="Seden Mutaf", 
                     show_label=False, 
                     show_download_button=False, 
                     container=False, 
                     height=120,
                     width=90)
        with gr.Column(scale=4):
            gr.Markdown("""
# 👩‍💻 Seden Mutaf  
**Senior CS student @ Özyeğin University**  
AI & Computer Vision Enthusiast  

📫 [LinkedIn](https://www.linkedin.com/in/seden-mutaf-91197b1b4/) | 🌐 [GitHub](https://github.com/sedenmutaf1)
            """)

    gr.ChatInterface(fn=chat, title="Ask Me Anything!")


demo.launch()
