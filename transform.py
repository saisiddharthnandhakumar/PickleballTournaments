import pandas as pd
import uuid
from datetime import datetime

df = pd.read_csv('extract_data.csv')

# Initialize an empty list to store partitioned dataframes
partitioned_dfs = []

# Iterate through each row in the 'Browse Row Data' column
for index, row in df.iterrows():
    text = row['Browse Row Data']
    
    # Partition by 'United States'
    parts = text.split('United States')
    
    # Take the part before 'United States' and strip any leading/trailing whitespace
    if len(parts) > 1:
        data_before_us = parts[0].strip()
        
        # Create a new DataFrame with the extracted data
        partitioned_df = pd.DataFrame({'Partitioned Data': [data_before_us]})
        
        # Append the partitioned DataFrame to the list
        partitioned_dfs.append(partitioned_df)

# Concatenate all partitioned DataFrames into a single DataFrame
result_df = pd.concat(partitioned_dfs, ignore_index=True)

#---------------------------------------------------------------------------

df_split = result_df['Partitioned Data'].str.split('\n', expand=True)

# Rename the columns
df_split.columns = ['Status', 'Date', 'Event', 'Details', 'City', 'State']

#------------------------------------------------------------------------------
def adjust_row(row):
    if pd.isna(row['State']):
        row['State'] = row['City']
        row['City'] = row['Details']
        row['Details'] = None
    return row

df_test = df_split.apply(adjust_row, axis=1)

def players_detail(row):
  if row['Details'] == None:
    row['Details'] = '0 players'
  return row

df_test = df_test.apply(players_detail, axis=1)
df_test

def extract_date(row):
    date_split = row['Date'].split(' - ')
    row['Start Date'] = date_split[0] if len(date_split) > 0 else None
    row['End Date'] = date_split[1] if len(date_split) > 1 else None
    return row

def fix_date(row):
    if pd.isna(row['End Date']) or row['End Date'] == '':
        row['End Date'] = row['Start Date']
    return row

df2 = df_test.apply(extract_date, axis = 1)
df3 = df2.apply(fix_date, axis = 1)

date_format = "%b %d %Y"

def convert_to_datetime(date_str):
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None  # Handle cases where date format does not match expected format

# Apply the function to the Start Date column
df3['Start Date'] = df3['Start Date'].apply(convert_to_datetime)
df3['End Date'] = df3['End Date'].apply(convert_to_datetime)

df3.drop('Date', axis = 1, inplace = True)
df3['Event'] = df3['Event'].str.replace(',', '')

df3['ID'] = [str(uuid.uuid4()) for _ in range(len(df3))]

cols = df3.columns.tolist()
cols = cols[-1:] + cols[:-1]
df3 = df3[cols]

df3.to_csv('bracket_data.csv', index = False, header = False)