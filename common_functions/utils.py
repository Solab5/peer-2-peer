## This file contains the common files used in the notebooks
import pandas as pd
from pathlib import Path
import streamlit as st

def gender_age_processing(df: pd.DataFrame):
    """
    Takes a dataframe and returns a preprocessed dataframe
    """
    # Create a new variable Gender
    df['Gender'] = df['Household_Head_Gender']
    
    if 'Gender' in df.columns and 'Household_Head_Age' in df.columns:
        df['Household_Head_Gender'] = df.apply(lambda row: 
            'Youth Headed' if row['Household_Head_Age'] <= 30 
            else (str(row['Household_Head_Gender']) + ' Headed') if not row['Household_Head_Gender'].endswith(' Headed') 
            else row['Household_Head_Gender'], axis=1)
        
        # Drop the unnecessary columns
        # df.drop(columns=['Gender'], inplace=True)
        df['HHHeadship'] = df['Household_Head_Gender']
    return df


def read_file(uploaded_file):
  """
  Takes a Streamlit uploaded_file object and returns a dataframe
  """

  # Extract filename and get extension
  filename = uploaded_file.name
  file_extension = Path(filename).suffix.lower()

  if file_extension in ('.csv', '.xls', '.xlsx'):
    if file_extension == '.csv':
      return pd.read_csv(uploaded_file)
    elif file_extension == '.xls' or file_extension == '.xlsx':
      return pd.read_excel(uploaded_file)
    else:
      raise ValueError("Unsupported file format. Only CSV and Excel files are supported.")
  else:
      st.error("Unsupported file format. Only CSV and Excel files are supported.")
        
def prepare_data(df):
    """
    Takes a dataframe and returns only the required columns,
    and adds extra columns needed in the final output.
    """
    columns = [
        'district',
        'subcounty',
        'parish_t',
        'cluster_t',
        'village',
        'lat_x',
        'long_y',
        'hhh_full_name',
        'Household_Head_Age',
        'Household_Head_Contact',
        'Gender',
        'HHHeadship',
        'maritalstatus',
        'spousename',
        'spouse_sex',
        'spouse_age',
        'spouse_contact',
        'home',
        'hhid',
    ]

    df_prepared = gender_age_processing(df.copy())

    # Backwards-compatibility for older extracts
    if 'spousename' not in df_prepared.columns and 'Spouse_Name' in df_prepared.columns:
        df_prepared['spousename'] = df_prepared['Spouse_Name']
    if 'spouse_contact' not in df_prepared.columns and 'Telephone_Contact' in df_prepared.columns:
        df_prepared['spouse_contact'] = df_prepared['Telephone_Contact']

    df_prepared = df_prepared[columns]

    return df_prepared