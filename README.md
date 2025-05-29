# 🧠 MCQ Generator with LangChain and Streamlit

This project lets you **automatically generate multiple choice questions (MCQs)** from uploaded PDF or text files using **OpenAI's GPT-3.5-turbo** model via **LangChain**. It's wrapped in an easy-to-use **Streamlit** web app.

---

## ✨ Features

- 📄 Upload `.pdf` or `.txt` files
- 🧠 Extracts content and generates MCQs using OpenAI
- 🔍 Reviews MCQs for complexity, grammar, and clarity
- 📊 Displays questions in a structured table
- 💾 Download the quiz as a CSV file

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/mcq-generator.git
cd mcq-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key
Create a file named `.env` in the root directory and add:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the app
```bash
streamlit run mcq_app.py
```

---

## 🖼️ App Preview

![App Screenshot](https://user-images.githubusercontent.com/example/screenshot.png)

---

## 🧾 Example Output

| MCQ | Choices | Correct |
|-----|---------|---------|
| What is the capital of France? | A→ Paris \|\| B→ London \|\| C→ Berlin \|\| D→ Madrid | A |

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) – for the UI
- [LangChain](https://www.langchain.com/) – for LLM integration
- [OpenAI](https://platform.openai.com/) – GPT-3.5-turbo model
- [PyPDF2](https://pypi.org/project/PyPDF2/) – for reading PDFs
- [Pandas](https://pandas.pydata.org/) – for table and CSV operations

---

## 📂 File Structure

```
mcq-generator/
├── mcq_app.py         # Main Streamlit app
├── requirements.txt   # Python dependencies
├── .env               # Your OpenAI key (not committed)
├── Response.json      # Sample format for output
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License.  
Feel free to use, modify, and share!

---

## 🙋‍♀️ Acknowledgements

Special thanks to:
- [OpenAI](https://openai.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
