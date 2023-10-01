import streamlit as st
import pandas as pd
import json
from collections import Counter
import re

def analyze_text(text):
    words = re.findall(r'\w+', text.lower())
    word_frequency = Counter(words)
    most_common_words = word_frequency.most_common(5)
    return most_common_words

def analyze_todo_list(text):
    lines = text.split('\n')
    urgent_tasks = [line for line in lines if "[Urgent]" in line]
    regular_tasks = [line for line in lines if "[Urgent]" not in line]
    return urgent_tasks, regular_tasks

def analyze_chatgpt_prompts(text):
    lines = text.split('\n')
    questions = [line for line in lines if "?" in line]
    statements = [line for line in lines if "?" not in line]
    return questions, statements

def main():
    st.title("LifeStream: The Language Chain of Your Life")
    
    file_type = st.selectbox("What type of file are you uploading?", ["To-Do List", "ChatGPT Prompts", "Other Text"])
    uploaded_file = st.file_uploader("Choose a CSV, TXT, or JSON file", type=['csv', 'txt', 'json'])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        if uploaded_file.type == 'text/csv':
            df = pd.read_csv(uploaded_file)
            st.write(df.head())
        elif uploaded_file.type == 'text/plain':
            text = uploaded_file.read().decode()
            st.write(text)
            
            if file_type == "To-Do List":
                st.subheader("To-Do List Analysis")
                urgent_tasks, regular_tasks = analyze_todo_list(text)
                st.write("Urgent Tasks:", urgent_tasks)
                st.write("Regular Tasks:", regular_tasks)
                
            elif file_type == "ChatGPT Prompts":
                st.subheader("ChatGPT Prompt Analysis")
                questions, statements = analyze_chatgpt_prompts(text)
                st.write("Questions:", questions)
                st.write("Statements:", statements)
                
            else:
                st.subheader("General Text Analysis")
                most_common_words = analyze_text(text)
                st.write(most_common_words)
        elif uploaded_file.type == 'application/json':
            json_data = json.load(uploaded_file)
            st.write(json_data)
            # Add more specific handling for ChatGPT JSON data here

if __name__ == '__main__':
    main()
