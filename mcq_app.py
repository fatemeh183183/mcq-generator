# -------------------------------
# MCQ Generator Web App with LangChain and Streamlit
# This app allows users to upload a text or PDF file,
# generate multiple choice questions (MCQs) using OpenAI's LLM,
# and review them for clarity and appropriateness.
# -------------------------------
import os
import json
import traceback
import logging
import pandas as pd
import PyPDF2
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.callbacks import get_openai_callback

# ------------------- Logging Setup -------------------
# Create a log file with timestamp in a "logs" folder
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)
# Configure logging to write INFO level logs to the file
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

# ------------------- File Reading -------------------
# Function to read text from uploaded PDF or TXT file
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file) # Updated to new PyPDF2 API
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception:
            raise Exception("Error reading PDF file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("Unsupported file format")
# ------------------- Data Formatting -------------------
# Convert quiz JSON string into a structured table for display
def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [f"{option}-> {option_value}" for option, option_value in value["options"].items()]
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

# ------------------- Environment & LLM Setup -------------------
# Load OpenAI API key from .env file
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
# Initialize OpenAI model
llm = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.3)

with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

# ------------------- Prompt Templates -------------------
# Template to generate MCQs based on text
template_gen = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to 
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""
# Template to evaluate and potentially revise MCQs
template_eval = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the test and give a complete analysis of the quiz if the students
will be able to understand the questions and answer them. Only use at max 50 words for complexity analysis.
If the quiz is not at par with the cognitive and analytical abilities of the students,
update tech quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQ:
{quiz}
Check from an expert English Writer of the above quiz:
"""
# ------------------- LangChain Chains -------------------
# Chain to generate MCQs
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "grade", "tone", "response_json"],
    template=template_gen
)
# Chain to review MCQs
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template_eval
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
# Sequential chain to run generation then evaluation
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)

# ------------------- Streamlit UI -------------------
st.title("MCQs Creator Application with LangChain 🦜️🔗")
# Input form for uploading file and entering parameters
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")
# ------------------- Form Submission Logic -------------------
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text = read_file(uploaded_file)
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
                # Logging token usage
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}")

            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)
                        #download csv file
                        csv= df.to_csv(index=False).encode('utf-8')
                        st.download_button("Download MCQS as CSV ",csv,"mcqs.csv","text/csv")
                        # Show review
                        st.text_area(label="Review", value=response["review"])
                    else:
                        st.error("Error in the table data")
            else:
                st.write(response)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error")
