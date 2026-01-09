# Financial Data Chatbot (Assessment Submission)

A robust, local AI chatbot designed to analyze financial datasets (`holdings.csv` and `trades.csv`). 

This solution uses a **Hybrid Architecture**:
1.  **Zero-Shot AI (BART):** To understand natural language and user intent.
2.  **Pandas Engine:** To perform 100% deterministic and accurate calculations.
3.  **Strict Guardrails:** Ensures the bot strictly replies *"Sorry can not find the answer"* if data is missing, preventing hallucinations.

---

## 🚀 Features

* **Privacy First:** Runs entirely locally using Hugging Face's `facebook/bart-large-mnli` model. No data leaves the machine; no API keys required.
* **Intent Classification:** Distinguishes between counting requests, performance analysis, greetings, and out-of-scope questions.
* **Smart Name Matching:** Handles complex fund names (e.g., distinguishing between "Platpot" and "Platpot Fund").
* **Performance Analysis:** Calculates Year-to-Date (YTD) Profit & Loss dynamically.
* **Strict Compliance:** Adheres to the assessment rule to never guess or use internet knowledge.

---

## 🛠️ Prerequisites

* **Python 3.8** or higher.
* **Memory:** At least 4GB RAM (to load the Transformer model).

---

## 📦 Installation & Setup

Follow these steps to set up the project in Visual Studio Code or your terminal.

### 1. Clone or Download Project
Ensure your project folder contains the following files:
* `chatbot.py` (The main script)
* `holdings.csv`
* `trades.csv`

### 2. Create a Virtual Environment
It is recommended to run this in a clean environment to avoid conflicts.

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate

**Install Requirements.txt:**
```bash 
pip install -r reuirements.txt

**Run the code**
```bash
python ./chatbot.py


Category,User Question,Expected Output
Counting,"""Total number of holdings or trades for Northpoint 401K""",Returns exact counts from both CSVs.
Performance,"""Which funds performed better depending on the yearly Profit and Loss""",Identifies the top fund based on PL_YTD.
Name Overlap,"""How many trades for Platpot?""","Correctly matches ""Platpot"" without confusing it with ""Platpot Fund""."
Negative Test,"""Who is the fund manager?""","""Sorry can not find the answer"""
Negative Test,"""What is the stock price of Apple?""","""Sorry can not find the answer"""