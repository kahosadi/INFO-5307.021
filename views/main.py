import streamlit as st
import pandas as pd
import json
from pathlib import Path
#from difflib import SequenceMatcher 
from pyjarowinkler import distance

import enapatitlecasechecker as ch
import keywordsabstract as kw

__data_path = str(Path.cwd()) + "/data/fla/items_fbs.json"
__data_path_auth = "D:\\OneDrive\\Master of Information Science-UNT\\3-Fall 2024\\INFO5307_021_Proj\\data\\fla\\name_authority_fbs.json"
metadata = []

def read_json(file_path):
    with open(file_path, 'r', errors="replace") as file:
        data = json.load(file)
        
    return data

__data = read_json(__data_path)
__data_auth = read_json(__data_path_auth)
    
def query_json(data, key):
    if not data:
        return []
       
    results = []
    for item in data:
        if not item["metadata"]:
            pass
        else:
            results.append([item["identifier"],item["metadata"][key]])

    return results

def query_json_metadata(data, key):
    if not data:
        return []
       
    results = []
    for item in data:
        if item["identifier"] == key:
            return item["metadata"]
    
    return results


def populate_selectbox(search_filter="Title"):
    #data = read_json("D:\\OneDrive\\Master of Information Science-UNT\\3-Fall 2024\\INFO5307_021_Proj\\data\\fla\\items_fbs.json")
    match search_filter:
        case "Title":
            return query_json(__data, "title")
        case "Author":
            return query_json(__data, "creator")
        #case "Advisor":
        #    pass

def evaluate_title(title):
    checker = ch.enapatitlecasechecker()
    return checker.check_apa_title_case(title)

def evaluate_keyword(keywords, abstract, threshold=0.1):
    results = []
    message = ""
    for keyword in keywords:
        res = kw.calculate_similarity(keyword, abstract)
        if res > threshold:
            message = f"Keyword '{keyword}' is a good match"
        else:
            message = f"Keyword '{keyword}' is not a good match"
        
        results.append(message)
        
    return results

def evaluate_advisor(advisor):
    results = []
    
    for name in __data_auth:
        if not name["authoritative_name"]:
            pass
        else:
            name_adv = "".join(advisor.lower().strip().split(",")[::-1])   #advisor.lower().strip().split(",")
            #name_adv = advisor.lower().strip().replace(",","")
            #name_aut = name["authoritative_name"].lower().strip().replace(",","")
            name_aut = "".join(name["authoritative_name"].lower().strip().split(",")[::-1])
                
            if name_adv == name_aut:
                results.append([name["authoritative_name"],float(1)])
                return results
            else:
                results.append([name["authoritative_name"],distance.get_jaro_distance(name_adv, name_aut, winkler=True, scaling=0.1)])
                
    return results
    

def format_option(option):
    return (option[1])
    
'''*******************************************************************************'''

st.title("Metadata Evaluator v0.1")

search_filter = st.radio("Search by",key="visibility",options=["Title","Author"])

option = st.selectbox(
    "Select",
    #options = [opt[1] for opt in populate_selectbox(search_filter)],
    options = populate_selectbox(search_filter),
    format_func=format_option,
    key = "items",
    index=None,
    placeholder="Select one " + search_filter.lower(),
    label_visibility="collapsed"
)

identifier = option[0] if option is not None else "" 

if identifier == "":
    st.button("Evaluate!",disabled=True)
else:
    btnExec = st.button(
        "Evaluate!",
        key="execute",
        disabled=False
    )

    if btnExec:
        
        metadata = query_json_metadata(__data, identifier)
        
        #Title
        
        st.subheader("Title")
        
        title_evaluation = evaluate_title(metadata["title"])
        if title_evaluation["is_valid"]:
            st.write("The title is valid!👍")
        else:
            st.write("🚨Please check the errors below:")
            st.write(title_evaluation["errors"])
        
        st.divider()
        
        #Advisor
        
        st.subheader("Advisors")
        
        if "contributor" not in metadata:
            st.write("🚨No advisors name supplied!")
        else:    
            advisors = metadata["contributor"]
            
            if type(advisors) is list:
                for advisor in advisors:
                    st.write(advisor)
                    
                    result_eval = evaluate_advisor(advisor)
                    result_eval.sort(key = lambda x: x[1], reverse=True)
                    
                    if result_eval[0][1] == 1:
                        st.write("      Advisor name authorized👍")    
                    else:
                        st.write("      🚨Advisor name NOT authorized")
                        if result_eval[0][1] > 0.9:
                            st.write(f"Do you mean '{result_eval[0][0]}'")
                        
                    #st.write(result_eval)
            else:
                st.write(advisors)
                
                result_eval = evaluate_advisor(advisors)
                result_eval.sort(key = lambda x: x[1], reverse=True)
                
                if result_eval[0][1] == 1:
                    st.write("      Advisor name authorized👍")    
                else:
                    st.write("      🚨Advisor name NOT authorized")
                    if result_eval[0][1] > 0.9:
                        st.write(f"Do you mean '{result_eval[0][0]}'")
        
        st.divider()
        
        #Abstract
        st.subheader("Abstract")
        abstract = ""
        if not metadata["description"]:
            st.write("No abstract available!")
        else:
            abstract = metadata["description"]
            st.write("Abstract available👍")
        st.divider()
        
        #Keywords
        st.subheader("Keywords")
        keywords = []
        
        if "subject" not in metadata:
            st.write("🚨No keywords available!")
        else:    
            keywords = metadata["subject"]
            
            if abstract != "":
                st.write(evaluate_keyword(keywords, abstract))
        
        
        
