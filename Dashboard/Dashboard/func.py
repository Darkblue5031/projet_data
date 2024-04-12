import pandas as pd

df = pd.read_csv("netflix_titles.csv")

def ratio(col:str, value:str):
    count =  (df[col] == value).sum()
    lengh_col = len(df)

    return (count / lengh_col) * 100
