import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def import_bank_data(bank_data_points):
    try:
        df = pd.read_csv(bank_data_points, encoding='utf8')
        print("Bank Account Data:")
        print(df.head(20))
        return df

    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def rank_within_four_days(value, values_within_four_days):
    # combine the target value in abs_amnt and the values within four days
    all_values = [value] + values_within_four_days
    # sort the combined list
    sorted_values = sorted(all_values)
    # find the index position of the original value in the sorted list
    rank = sorted_values.index(value)
    return rank / len(sorted_values)

file_path = '/Users/luziarode/Desktop/bank_data_points.CSV'
bank_data = import_bank_data(file_path)

if bank_data is not None:
    # convert the 'date' column to datetime format
    bank_data['date'] = pd.to_datetime(bank_data['date'], format='%d.%m.%y')

    # Sort the df by 'date' column
    bank_data = bank_data.sort_values(by='date')

    # create a new column for rank within the last four days
    bank_data['rank_within_four_days'] = np.nan

    # iterate over each row in the df
    for index, row in bank_data.iterrows():
        value = row['abs_amnt']
        # extract the date of the expenditure
        expenditure_date = row['date']
        # get all the values within four days of the expenditure date
        values_within_four_days = bank_data[(bank_data['date'] >= expenditure_date - pd.Timedelta(days=10)) & (bank_data['date'] <= expenditure_date)]['abs_amnt'].tolist()
        # calculate rank within the last four days
        rank = rank_within_four_days(value, values_within_four_days)
        # assign the rank to the corresponding row
        bank_data.at[index, 'rank_within_four_days'] = rank

    # print the updated df
    print("Updated Bank Account Data:")
    print(bank_data.head(20))

    # create plot
    plt.figure(figsize=(10, 6))
    plt.scatter(bank_data['abs_amnt'], bank_data['rank_within_four_days'], alpha=0.5)
    plt.title('Scatter Plot of Rank vs Abs_amnt (Within Last 10 Days)')
    plt.xlabel('Abs_amnt')
    plt.ylabel('Rank (Within Last Four Days)')
    plt.grid(True)
    plt.show()
