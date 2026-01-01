import pandas as pd

def export_keywords_df(research_data: dict):
    return pd.DataFrame(research_data["keywords"])