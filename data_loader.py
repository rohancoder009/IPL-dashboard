import pandas as pd

def load_ipl(path='D:/data science/Projects/IPl/datasets/cleanandmerged.csv'):
    return pd.read_csv(path)
def load_matches(path='D:/data science/datasets/ipl/matches.csv'):
    return pd.read_csv(path)
