import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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
df_Q1 = df_Q1["Description"]

pie_chart = px.pie(df_Q1,
                   title="Juridical Form",
                   values="Description",
                   names="Description")

Piechart_Jurid = st.plotly_chart(pie_chart)
Piechart_Jurid