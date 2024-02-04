import json
from difflib import get_close_matches
import streamlit as st
import numpy as np
import subprocess
def load_data(filepath : str):
    with open(filepath,"r") as datafile :
        data = json.load(datafile)
        return data

import arabic_reshaper
from bidi.algorithm import get_display

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
    
    data = load_data("D:\Project\chat-bot\dataset\data.json")


    userinput =pm
    bestmatch = find_best_question(userinput,[q["question"] for q in data["questions"]])

    if bestmatch:
        answer = find_best_answer(bestmatch,data)
       
        
    else:
           
            av = "من جواب اینو نمیدونم میتونی بهم یاد بدی؟"
            st.markdown(av)
            jm = st.chat_input("یا جواب رو وارد کن یا بنویس'نمیخوام ")
            
            newanswer = jm

            if newanswer != "نمیخوام":
                newdata = {"question":userinput , "answer" : newanswer}
                data["questions"].append(newdata)
                save_data("data.json",data)
                with st.chat_input("جواب"):
                    st.write("ربات : ممنون که جوابو به من یاد دادی")
    return answer

if __name__  == "__main__":

    st.title("ارتباط با پشتیبانی")
        

    st.markdown(
        """
        <style>
            body {
                direction: rtl;
                text-align: right;
            }
        </style>
        """,
    unsafe_allow_html=True)
    
            
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages :

        with st.chat_message(message["role"]):
            st.markdown(message["content"])
                
    if pm := st.chat_input("پیام بنویس"):
        jm = chatbot(pm)
        st.session_state.messages.append({"role":"user","content":pm})
        with st.chat_message("user"):
                    
            st.markdown(pm)
        with st.chat_message("assistant"):
            st.markdown(jm)
        

