import pandas as pd


def get_crop_npk(crop, days):
    days_diff = days
    if crop == "Chilli":
        df = pd.read_csv('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python Project\\'
                         'chilli_mg_npk.csv', index_col='days')
        days_diff = days
    if crop == "Tomato":
        df = pd.read_csv('G:\\UOC FOT\\8th-Semester\\IA 4050 Research Project\\Python Project\\'
                         'tomato_mg_npk.csv', index_col='days')
        days_diff = days
    return df.iloc[days_diff]


# Nitrogen recommendation
def nitrogen_decision(nitrogen_recommend, nitrogen_sensor):
    # Define the threshold as +/- 5%
    threshold_percentage = 5

    # Calculate the acceptable range
    upper_limit = nitrogen_recommend * (1 + threshold_percentage / 100)
    lower_limit = nitrogen_recommend * (1 - threshold_percentage / 100)

    # Check if the nitrogen value is within the acceptable range
    if lower_limit <= nitrogen_sensor <= upper_limit:
        return "Monitor"
    elif nitrogen_sensor > upper_limit:
        return "No need to fertilize"
    else:
        return "Fertilize"


def phosphorus_decision(phosphorus_recommend, phosphorus_sensor):
    # Define the threshold as +/- 5%
    threshold_percentage = 5

    # Calculate the acceptable range
    upper_limit = phosphorus_recommend * (1 + threshold_percentage / 100)
    lower_limit = phosphorus_recommend * (1 - threshold_percentage / 100)

    # Check if the nitrogen value is within the acceptable range
    if lower_limit <= phosphorus_sensor <= upper_limit:
        return "Monitor"
    elif phosphorus_sensor > upper_limit:
        return "No need to fertilize"
    else:
        return "Fertilize"


def potassium_decision(potassium_recommend, potassium_sensor):
    # Define the threshold as +/- 5%
    threshold_percentage = 5

    # Calculate the acceptable range
    upper_limit = potassium_recommend * (1 + threshold_percentage / 100)
    lower_limit = potassium_recommend * (1 - threshold_percentage / 100)

    # Check if the nitrogen value is within the acceptable range
    if lower_limit <= potassium_sensor <= upper_limit:
        return "Monitor"
    elif potassium_sensor > upper_limit:
        return "No need to fertilize"
    else:
        return "Fertilize"
