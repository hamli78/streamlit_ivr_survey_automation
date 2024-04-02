import pandas as pd
import numpy as np

def process_file(uploaded_file):
    """
    Process the uploaded CSV file to extract and transform phone number data
    and user response data for analysis.
    
    The function performs several steps:
    - Reads the CSV, skipping the first row and setting column names dynamically.
    - Drops columns that are entirely NA.
    - Extracts columns for phone numbers and user responses.
    - Identifies total number of calls and total pickups.
    - Filters data to complete responses where a user key press is recorded.
    - Adds a 'Set' column to indicate data belonging to the IVR set.
    - Filters for records where the user key press response is exactly 10 characters long.

    Parameters:
    - uploaded_file: A file-like object representing the uploaded CSV file.
                     This object must support file-like operations such as read.

    Returns:
    - A tuple containing:
        - df_complete: A pandas DataFrame of the processed data, with calls that have complete information.
        - phonenum_list: A pandas DataFrame containing the list of phone numbers that have at least one user key press.
        - total_calls: The total number of calls (rows) in the uploaded file.
        - total_pickup: The total number of calls where a user key press was recorded.

    Note:
    - The function assumes the uploaded CSV has specific columns of interest, notably 'PhoneNo' and 'UserKeyPress'.
    - It is assumed that the second row of the CSV provides the column names for the data.
    """
    df_list = []
    phonenum_list = []
    total_call_made = []
    total_calls_made = []
    total_of_pickup = []
    total_of_pickups = []
    i = 0
    
    df = pd.read_csv(uploaded_file, skiprows=1, names=range(24), engine='python')

    # Drop all-empty columns
    df.dropna(axis='columns', how='all', inplace=True)

    # Assign first row as column names
    df.columns = df.iloc[0]

    # Select PhoneNo column and all columns from UserKeyPress onwards
    df_phonenum = df[['PhoneNo']]
    df_response = df.loc[:, 'UserKeyPress':]
    df_results = pd.concat([df_phonenum, df_response], axis='columns')

    # Count total calls made
    df_results.drop_duplicates(subset=['PhoneNo'], inplace=True)
    total_call_made = len(df_results)
    total_calls_made.append(total_call_made)

    # Drop rows with blank response in the first question only
    phonenum_recycle = df_results.dropna(subset=['UserKeyPress'])

    # Append the participated phone no. into phonenum_list (select PhoneNo column only)
    phonenum_list.append(phonenum_recycle[['PhoneNo']])

    # Drop incomplete rows
    df_complete = df_results.dropna(axis='index')

    # Count the total pickup
    total_of_pickup = len(df_complete)
    total_of_pickups.append(total_of_pickup)

    # Reset column names for accurate concatenation later
    df_complete.columns = np.arange(len(df_complete.columns))

    # Initialize `Set` column
    df_complete['Set'] = 'IVR'

    # Select all columns from the first one up to `Cluster`
    df_complete = df_complete.loc[:, :'Set']

    # Filter out key presses that are blank
    df_complete = df_complete.loc[(df_complete.iloc[:, 2].str.len() == 10)]

    # Append the CRs into df_list (to be used later)
    df_list.append(df_complete)

    # Get the total number of completed responses
    df_merge = pd.concat(df_list, axis='index')

    # Combined all participated phone no. stored in phonenum_list
    phonenum_combined = pd.concat(phonenum_list, axis='rows')

    # Rename column to match with codes in databricks
    phonenum_combined.rename(columns={'PhoneNo': 'phonenum'}, inplace=True)

    return df_merge, phonenum_list, total_calls_made, total_of_pickups
