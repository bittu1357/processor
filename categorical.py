import pandas as pd

def categorical_info(df):
    s = (df.dtypes == 'object')
    object_cols = list(s[s].index)
    return object_cols  

def ohe(df,name):
    dummies=pd.get_dummies(df[name])
    dummies.columns = name+"_" + dummies.columns
    merged=pd.concat([df,dummies],axis='columns')
    final=merged.drop(name,axis='columns')
    return final
