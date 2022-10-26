import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg

#connect to the SQL database
connection = sqlite3.connect('bce.db')


## QUESTION 2

#query tables : Which percentage of the companies are under which Status?
sql_query_Q2 = pd.read_sql_query ('''
                               SELECT count(EnterpriseNumber), Status
                               FROM enterprise
                               ''', connection)
#Create dataframe
df_Q2 = pd.DataFrame(sql_query_Q2)
score_active_ent = df_Q2.iat[0,0]

#Display the number of active company

st.markdown(f"<h1 style='text-align: center; color: blue;'>The number of active enterprise is :  </h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: lightblue;'>{score_active_ent} </h1>", unsafe_allow_html=True)


## QUESTION 1

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



### Question 3

#query tables : Which percentage of the companies are which type of entreprise?
sql_query_Q3T1 = pd.read_sql_query ('''
                               SELECT count(EnterpriseNumber), TypeOfEnterprise
                               FROM enterprise
                               Group by TypeOfEnterprise
                               ''', connection)

sql_query_Q3T2 = pd.read_sql_query ('''
                               SELECT *
                               FROM code
                               WHERE Language=="FR" AND Category=="TypeOfEnterprise"
                               ''', connection)

df_Q3T1 = pd.DataFrame(sql_query_Q3T1)
df_Q3T1.rename(columns = {'TypeOfEnterprise':'Code'}, inplace = True)
df_Q3T2 = pd.DataFrame(sql_query_Q3T2)
df_Q3 = pd.merge(df_Q3T1, df_Q3T2, on='Code')
df_Q3 = df_Q3[["count(EnterpriseNumber)", "Description"]]

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = df_Q3["Description"]
sizes = df_Q3["count(EnterpriseNumber)"]

fig3, ax3 = plt.subplots()
ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig3)