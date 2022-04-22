from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd



def minmax_df(df):
    scaler = MinMaxScaler()
    names = df.columns
    d = scaler.fit_transform(df)
    scaled_df = pd.DataFrame(d, columns=names)
    return scaled_df


def minmax_column(df,name):
    scaler = MinMaxScaler()
    df[[name]]= scaler.fit_transform(df[[name]])
    return df

def standardscaler_df(df):
    scaler = StandardScaler()
    names = df.columns
    d = scaler.fit_transform(df)
    scaled_df = pd.DataFrame(d, columns=names)
    return scaled_df

def standardscaler_column(df,name):
    scaler = StandardScaler()
    df[[name]] = scaler.fit_transform(df[[name]])
    return df


# standard_df = pd.DataFrame(standard_df, columns =['x1', 'x2'])



# scaled_features = data.copy()
 
# col_names = ['Age', 'Weight']
# features = scaled_features[col_names]
# scaler = StandardScaler().fit(features.values)
# features = scaler.transform(features.values)
 
# scaled_features[col_names] = features