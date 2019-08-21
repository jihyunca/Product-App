import pandas as pd
data = pd.read_csv(r'/Users/amansingh/Desktop/Product-App/app/sample.csv')
cond = (data['BRAND'].str.contains('MINA'))
data.loc[cond, 'CONCAT'] = data['CONCAT'] + ' ' + 'HALAL'
data[data['CONCAT'].str.contains('HALAL')]

 

cond_two = ((data['BRAND'].str.contains('LIGHTLIFE')) | (data['BRAND'].str.contains('FIELD ROAST')))
data.loc[cond_two, 'CONCAT'] = data['CONCAT'] + ' ' + 'VEGGIE'

 

data.to_csv(r'/Users/amansingh/Desktop/Product-App/app/sample.csv')