import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt



#connect to the SQL database
connection = sqlite3.connect('bce.db')
#query tables
sql_query_Q1T1 = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM enterprise
                               ''', connection)
#Create a dataframe 1 to prepare graph input
df_Q1T1 = pd.DataFrame(sql_query_Q1T1, columns = ['EnterpriseNumber', 'JuridicalForm'])

#query table 2
sql_query_Q1T2 = pd.read_sql_query ('''
                               SELECT
                               *
                               FROM code
                               ''', connection)

#Create a dataframe 2 to prepare graph input
df_Q1T2 = pd.DataFrame(sql_query_Q1T2)
df_Q1T2 = df_Q1T2[df_Q1T2.Language.eq("FR")]
df_Q1T2 = df_Q1T2[df_Q1T2["Category"]=="JuridicalForm"]
df_Q1T2.rename(columns = {'Code':'JuridicalForm'}, inplace = True)

#Merge
df_Q1 = pd.merge(df_Q1T1, df_Q1T2, on='JuridicalForm')
df_Q1 = df_Q1[["Description"]]
df_Q1["Count"]= df_Q1.groupby("Description")["Description"].transform("count")
df_Q1 = df_Q1.drop_duplicates()
df_Q1['percent'] = (df_Q1['Count'] / df_Q1['Count'].sum()) * 100
df_Q1 = df_Q1[["Description", "percent"]]


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = df_Q1["Description"]
sizes = df_Q1["percent"]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)