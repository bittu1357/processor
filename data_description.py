def desc(df):
  df1=df.describe(include='all')
  return df1

def desc_s(df,text):
  df1=df[text]
  df2=df1.describe()
  return df2

def show_data(df):
  df1=df
  return df1