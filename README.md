# 🧠 Dataset Analyser using LangChain and Gemini

This project is an interactive dataset analysis tool powered by **LangChain** and **Google Gemini**. It automatically generates Pandas expressions for natural language queries on a CSV dataset, executes them, and explains the results in plain English.


## 📂 Project Structure
```text
dataset-analyser/
│
├── data/
│   └── employees.csv              # Sample dataset
│
├── src/
│   ├── main.py                    # Entry point for running the project
│   ├── config.py                  # Loads environment and initializes LLM
│   ├── schema.py                  # Defines the TypedDict schema (State)
│   ├── prompts.py                 # Stores all ChatPromptTemplate definitions
│   ├── pipeline.py                # Contains all functions and chain logic
│
├── requirements.txt               # Required Python libraries
└── README.md                      # Project documentation
```

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/<your-username>/dataset-analyser.git
cd dataset-analyser

### 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt


### 🚀 Run the Project
cd src
python dataset_analyser.py

Example usage:
Enter your query about dataset: show average salary by department

To exit:
Enter your query about dataset: quit


