def remove_col(df,text):
    df1=df.drop(columns=text)
    return df1

    
def f_null(df):
    missing_values_count = df.isnull().sum()
    return missing_values_count

def fill_na_mean(df,colname):
    df[colname].fillna(value=df[colname].mean(), inplace=True)
    return df

def fill_na_median(df,colname):
    df[colname].fillna((df[colname].median()), inplace=True)
    return df

def fill_na_mode(df,colname):
    df[colname].fillna((df[colname].mode()), inplace=True)
    return df