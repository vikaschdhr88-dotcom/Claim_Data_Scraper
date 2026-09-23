import pandas as pd

def read_input(file_path):
    return pd.read_excel(file_path)

def save_output(records, file_path):

    df = pd.DataFrame(records)

    df.to_excel(file_path, index=False)

    print(f"Output saved : {file_path}")