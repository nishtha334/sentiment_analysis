import pandas as pd

df=pd.read_csv("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products.csv")

# print(df.iloc[150]['name'])

# print("------------------------------")

new_df=df[df['name']=='Amazon - Echo Plus w/ Built-In Hub - Silver'] #put here name what we want
filtered_df=new_df[['reviews.text','reviews.date','reviews.rating']]

filtered_df.to_csv("newone.csv", index=False)

# Amazon Kindle E-Reader 6" Wifi (8th Generation, 2016)