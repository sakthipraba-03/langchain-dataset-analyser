# 🧠 Dataset Analyser using LangChain and Gemini

This project is an interactive dataset analysis tool powered by **LangChain** and **Google Gemini**. It automatically generates Pandas expressions for natural language queries on a CSV dataset, executes them, and explains the results in plain English.


## 📂 Project Structure
```text
dataset-analyser/
│
├── data/
│   └── employees.csv              # sample dataset
│
├── src/
│   └── dataset_analyser.py        # main project code
│
├── requirements.txt               # required Python libraries
└── README.md                      # project documentation
```

> **Note:** The `.env` file is **not inside this folder**.  
> In this project, the environment file is located in another directory, and it is accessed directly through the path specified in your code:
> ```python
> load_dotenv("../Langchain/.env")
> ```
> This means the code reads your API key from that external `.env` file and does not require a local `.env` file in this folder.


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


