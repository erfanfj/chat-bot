import json
from difflib import get_close_matches
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

def chatbot():
    data = load_data("D:\Project\chat-bot\dataset\data.json")


    while True:
        userinput = convert(input(convert("شما : "))).lower()
        if userinput == "quit":
            break
    

        bestmatch = find_best_question(userinput,[q["question"] for q in data["questions"]])

        if bestmatch:
            answer = find_best_answer(bestmatch,data)
            print(convert("ربات: "),answer)
        
        else:
            print(convert("من جواب اینو نمیدونم میتونی بهم یاد بدی؟"))
            newanswer = convert(input(convert("'یا جواب رو وارد کن یا بنویس'نمیخوام "))).lower()

            if newanswer != convert("نمیخوام"):
                newdata = {"question":userinput , "answer" : newanswer}
                data["questions"].append(newdata)
                save_data("data.json",data)
                print(convert("ربات : ممنون که جوابو به من یاد دادی"))

if __name__ == "__main__":
    chatbot()
