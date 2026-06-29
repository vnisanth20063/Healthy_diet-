# 🩺 Health AI Report Analyzer & Diet Planner

## 📌 Project Overview

Health AI Report Analyzer & Diet Planner is an AI-powered healthcare assistant that analyzes medical report information and generates personalized health insights and diet recommendations.

The application uses Large Language Models (LLMs) to extract important medical values, identify abnormal health indicators, provide simple report summaries, and create customized diet plans based on user details such as age, gender, activity level, and existing health conditions.

The goal of this project is to make medical information easier to understand and provide AI-assisted health recommendations.


# ✨ Features

- 📄 Medical report analysis using LLM
- 🔍 Extracts important health values from reports
- ⚠️ Identifies abnormal values and explains them simply
- 🧠 Generates AI-based health summaries
- 🥗 Creates personalized diet plans
- 👤 Uses user details for customized recommendations
- 🔐 Secure API key handling
- ⚡ Optimized AI model loading using caching
- 🖥️ Interactive Streamlit web application


# 🏗️ Architecture / Workflow

The application follows a multi-step AI workflow:

```
User Input
     ↓
Medical Report + Personal Health Details
     ↓
Input Validation
     ↓
LLM Medical Analysis
     ↓
Store Result using Session State
     ↓
Pass Analysis to Diet Generation Pipeline
     ↓
LLM Generates Personalized Diet Plan
     ↓
Display Results
```


## 🧠 AI Pipeline

### 1. Medical Report Analyzer

The user provides:

- Medical report text
- Age
- Gender
- Activity level
- Existing diseases


The LLM processes the information and generates:

- Extracted important values
- Abnormal values
- Simple health summary


### 2. Diet Planner

The medical analysis output is passed to the diet generation module.

The AI generates:

- Morning routine
- Breakfast suggestions
- Lunch plan
- Evening snacks
- Dinner recommendations
- Foods to eat
- Foods to avoid
- Lifestyle tips


# 🛠️ Tech Stack

## Programming Language

- Python


## Frontend

- Streamlit


## AI Technologies

- LangChain
- Groq API
- Llama 3.1 LLM


## Security & Configuration

- python-dotenv
- Environment Variables


## Concepts Used

- Prompt Engineering
- LLM Integration
- AI Workflow Design
- Session State Management
- Resource Caching


# 📂 Project Structure

```
Health-AI/
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```


# 🔑 Environment Setup

Create a `.env` file in the project folder:

```env
GROQ_API_KEY=your_api_key_here
```


# ▶️ Run the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```


# 🚀 Future Improvements

- 📑 Support PDF medical report uploads
- 🖼️ Extract data from medical report images using OCR
- 💬 Add conversational health chatbot
- 🤖 Implement Agentic AI workflow
- 📊 Add health analytics dashboard
- 👤 Add user authentication and history tracking
- 🌐 Deploy as a scalable cloud-based AI healthcare assistant


# 👨‍💻 Author

V Nisanth