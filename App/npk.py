import pandas as pd


def get_crop_npk(crop, days):
    days_diff = days
    if crop == "Chilli":
        df = pd.read_csv('App\\chilli_NPK.csv', index_col='Days')
        days_diff = days
    if crop == "Tomato":
        df = pd.read_csv('App\\tomato_NPK.csv', index_col='Days')
        days_diff = days
    return df.iloc[days_diff]
