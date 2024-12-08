import streamlit as st
import pandas as pd
import json
from pathlib import Path

def json_to_dataframe(file_path):
    try:
        # Read JSON file
        with open(file_path, 'r') as file:
            # Load JSON data
            data = json.load(file)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        return df
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

data_path = str(Path.cwd())+"/data/fla/name_authority_fbs.json"

st.title("Name Authority Headings")
st.dataframe(json_to_dataframe(data_path), hide_index=True, selection_mode="single-row")
