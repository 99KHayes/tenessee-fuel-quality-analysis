import pandas as pd

def volatilty_ASTM_df_creator(routine_csv, ASTM_csv):
    """Takes in the original csvs including the path names as strings for the results and ASTM standards. Saves the final df as volatility_gas_ASTM.csv in the processed data folder.

        Keyword arguments:
        routine_csv -- the name of the csv where all of the annual results are saved,
        ASTM_csv -- the name of the csv where all of the ASTM results are saved
    """

    # Makes the routine data frame to only gasoline and the desired volatility tests
    concat_df = pd.read_csv(routine_csv)
    gasoline_df = concat_df[concat_df.Prod == 'Gasoline']
    #print(gasoline_df.head())
    gasoline_df.DateSampled = pd.to_datetime(gasoline_df.DateSampled)
    gasoline_date_index_df = gasoline_df.set_index(gasoline_df.DateSampled)
    #
    gasoline_date_index_df[(gasoline_date_index_df.Test == 'Distillation 50%') | (gasoline_date_index_df.Test == 'Vapor Pressure') | (gasoline_date_index_df.Test == 'Vapor-Liquid Ratio')]
    #print(gasoline_date_index_df.head())
    full_volitility_df = gasoline_date_index_df.copy()
    print(full_volitility_df.head())
    full_volitility_df['datesampled_month'] = full_volitility_df['DateSampled'].dt.month
    full_volitility_df['datesampled_day'] = full_volitility_df['DateSampled'].dt.day
    full_volitility_df['datesampled_month_day'] = full_volitility_df['datesampled_month'].astype('str') + '/' + full_volitility_df['datesampled_day'].astype('str')
    full_volitility_df.rename(columns={'datesampled_month_day' : 'Date'}, inplace = True)
    (full_volatility_df.head())
    # Reads in the ASTM data which was transfered from the standard to an Excel file
    ASTM_df = pd.read_csv('../../data/01_raw/ASTM_fuel.csv')
    ASTM_df = ASTM_df.set_index(ASTM_df.Date)
    # Merge the two together
    new_volitility_df = full_volitility_df.merge(ASTM_df, how='left', on='Date')

    # Save to csv
    # volitility_df.to_csv('../../data/03_processed/volatility_gas_ASTM_function.csv')

    return new_volatility_df


def date_results_df_creator(df, test_name):
    """Takes in the file path of the large combined gasoline and ASTM standards dataframe. It makes the dateStamp in datetime form and on the index. Also takes the test of the specific test to be made into a df

        Keyword arguments:
        df -- the string of where the combined df is stored
        test_name -- the name of the test results to be tracked by date
    """

    volatility_df = pd.read_csv(df)
    volatility_df['DateSampled'] = pd.to_datetime(volatility_df.DateSampled).apply(lambda x: x.date())
    volatility_df = volatility_df.set_index(volatility_df.DateSampled)
    volatility_results_df = volatility_df[['Test','Result']]
    volatility_results_df['Result'] = volatility_results_df.Result.replace('  ', np.nan)
    volatility_results_df['temp'] = volatility_results_df.Result.astype('float')
    volatility_results_df.drop('Result', axis=1, inplace=True)
    volatility_results_floats_df = volatility_results_df.dropna()

    test_df = volatility_results_floats_df[volatility_results_floats_df.Test == test_name]
    test_df.rename(columns={"temp": "Result_deg_C"}, inplace =True)
    testing_df = test_df.drop(columns=['Test'])

    return testing_df
