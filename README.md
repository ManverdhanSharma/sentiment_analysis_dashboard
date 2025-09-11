# 🤖 CerebraViz – Sentiment Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask/Dash-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

CerebraViz is a **web-based sentiment analysis dashboard** that performs **real-time text analysis** and visualizes the results with **interactive charts**.

---

## ✨ Overview

This project provides a **user-friendly interface** to analyze the sentiment of any given text.  
The backend processes the input, classifies the sentiment as **Positive**, **Negative**, or **Neutral**, and the frontend displays the breakdown in a clean and interactive dashboard.  

![Dashboard Screenshot](screenshots/dashboard.png)  
*(Replace this with your actual dashboard screenshot)*

---

## 🚀 Features

- ⚡ **Real-time Analysis** – Instantly analyze sentiment of text inputs.  
- 📊 **Interactive Visuals** – Dynamic charts (pie charts, bar graphs) for clear insights.  
- 🧩 **Modular Codebase** – Well-structured files for easier maintenance and extension.  
- ⚙️ **Lightweight & Fast** – Built on Flask/Dash with minimal dependencies.  

---

## 📂 Project Structure

cerebravviz/
├── .gitignore # Files ignored by Git
├── LICENSE # Project license (MIT)
├── app.py # Main application (Flask/Dash server)
├── chart_generator.py # Chart creation logic
├── data_processor.py # Text preprocessing & cleaning
├── requirements.txt # Python dependencies
└── sentiment_analyzer.py # Core sentiment analysis logic

yaml
Copy code

---

## 🛠️ Technologies Used

- **Programming Language**: Python  
- **Framework**: Flask / Dash  
- **Data Visualization**: Plotly / Matplotlib  
- **Sentiment Analysis**: NLTK / TextBlob / Transformers  

---

## ⚙️ Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ManverdhanSharma/cerebravviz.git
cd cerebravviz
2. Create and Activate a Virtual Environment
Windows:

bash
Copy code
python -m venv venv
venv\Scripts\activate
macOS/Linux:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
▶️ How to Run
bash
Copy code
python app.py
Then open your browser at:
👉 http://127.0.0.1:5000

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

👨‍💻 Author
Manverdhan Sharma
🔗 [GitHub](https://github.com/ManverdhanSharma)  
🔗 [LinkedIn](https://www.linkedin.com/in/manverdhan-sharma-94aa0a2b1/)
