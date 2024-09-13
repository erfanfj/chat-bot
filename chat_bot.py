import json
from difflib import get_close_matches
import streamlit as st
import numpy as np
import subprocess
import time 
from streamlit_option_menu import option_menu
from PIL import Image
import arabic_reshaper
from bidi.algorithm import get_display


def load_data(filepath : str):
    with open(filepath,"r") as datafile :
        data = json.load(datafile)
        return data


def convert(text):
    reshaped_text = arabic_reshaper.reshape(text)
    converted = get_display(reshaped_text)
    return converted


def save_data(filepath : str , data : dict):
    with open(filepath,"w") as datafile :
        json.dump(data , datafile, indent=2)


def find_best_question(userquestion : str ,question: list[str]):
    matches = get_close_matches(userquestion,question,n=1 , cutoff=0.8)
    return matches[0] if matches else None

def find_best_answer(question : str , data : dict):
    for q in data["questions"]:
        if q["question"] == question:
            return q["answer"]


def chatbot(pm):
    # اجرای دستور ollama و باز کردن یک فرآیند
    process = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,  
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        text=True,
        encoding='utf-8'  # اضافه کردن این خط برای اطمینان از استفاده از UTF-8
    )

    output, error = process.communicate(input=pm)

    return output


if __name__  == "__main__":
    import base64

    st.title(":red[_Erfan GPT_]")

    image = Image.open("C:/Users/erfan/Downloads/photo_2024-09-06_17-29-41-removebg-preview.png")
    
    with open("C:/Users/erfan/Downloads/photo_2024-09-06_17-29-41-removebg-preview.png", "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

        st.sidebar.markdown(
            f"""
            <div style="display:table;margin-top:-12%;margin-left:1%;">
                <img src="data:image/png;base64,{data}" width="150" height="150">
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <style>
            body {
                direction: ltr;
                text-align: left;
            }
        </style>
        """,
    unsafe_allow_html=True)

    with st.sidebar:

        selected = option_menu(None, ["Home", "Upload", "Tasks", 'Settings' ,'New_chat'], 
        icons=['house', 'cloud-upload', "list-task", 'gear' , "pencil"], 
        menu_icon="cast", default_index=0, orientation="horizontal")
        
        if selected == "New_chat":
            selected_chat = option_menu(None,["caht 1"],icons = ["pencil"],menu_icon="cast", default_index=0, orientation="horizontal")
        if selected == "Upload":
            uploaded_file = st.file_uploader("Choose a file or image")

            
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages :

        with st.chat_message(message["role"]):
            st.markdown(message["content"])
                
    if pm := st.chat_input("message"):
        with st.chat_message("user"):
            st.markdown(pm)
        jm = chatbot(pm)
        st.session_state.messages.append({"role":"user","content":pm})
    
        with st.chat_message("assistant"):
            placeholder = st.empty()
            z = ''
            g = " "
            for word in jm.split():
                z+=word + g
                placeholder.markdown(z, unsafe_allow_html=True)
                time.sleep(0.2)
        st.session_state.messages.append({"role":"assistant","content":jm})
        

