import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import textwrap
import seaborn as sns
import os
from matplotlib.backends.backend_agg import RendererAgg

#connect to the SQL database
connection = sqlite3.connect('bce.db')

#configuration of the page
st.set_page_config(page_title="Business insights from active companies in Belgium", page_icon="https://www.executivechronicles.com/wp-content/uploads/2021/05/Business-Insights-and-Analytics.jpg", layout="wide", initial_sidebar_state="auto", menu_items=None)


## QUESTION 2
@st.cache(allow_output_mutation=True)
def get_data_enterprise():
    return pd.read_sql_query ('''
                               SELECT count(EnterpriseNumber) as Enterprise, Status
                               FROM enterprise
                               ''', connection)
#Create dataframe
df_Q2 = get_data_enterprise()
#Calculating percentage
df_Q2['Percentage'] = (df_Q2['Enterprise']/df_Q2['Enterprise'].sum()) * 100
#Assigning scores into values
score_active_ent = df_Q2.iat[0,0]
score_active_ent_prc = int(df_Q2.iat[0,2])
#Printouts into streamlit
st.markdown(f"<h1 style='text-align: center; color: darkgrey;'>SNAPSHOT OF</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: darkblue;'> {score_active_ent} </h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; color: darkgrey;'>ACTIVE ENTERPRISES IN BELGIUM </h3>", unsafe_allow_html=True)
#st.markdown(f"<h2 style='text-align: center; color: grey;'>{score_active_ent_prc}% ({score_active_ent}) </h1>", unsafe_allow_html=True)
st.markdown("##")
st.markdown("##")
st.markdown("##")
st.markdown("##")



## QUESTION 1
@st.cache(allow_output_mutation=True)
def get_data_enterprise_code():
        return pd.read_sql_query ('''
                                SELECT count(EnterpriseNumber) as Total_Enterprise, Description
                                FROM enterprise
                                INNER JOIN code ON enterprise.JuridicalForm = code.Code
                                WHERE code.Language = 'FR' AND code.Category = 'JuridicalForm'
                                Group by Description
                                Order by count(EnterpriseNumber) DESC;
                                ''', connection)

#Prepare data for printouts
df_Q1T1 = get_data_enterprise_code()
df_Q1T1_most_frequent = df_Q1T1.iloc[:6,:]
data = [{'Description':'Autres','Total_Enterprise':df_Q1T1['Total_Enterprise'][6:].sum()}]
data_df = pd.DataFrame(data)
df_Q1T1 = pd.concat([df_Q1T1_most_frequent, data_df])

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
# st.sidebar.header('Select what to display')
# type_of_enterprise = df_Q1T1['Description'].unique().tolist()
# type_selected = st.sidebar.multiselect('Type of enterprise', type_of_enterprise, type_of_enterprise)
# st.write('You selected:', type_selected)
plt.style.use('ggplot')
fig1, ax1 = plt.subplots()
ax1.pie(df_Q1T1['Total_Enterprise'], labels = df_Q1T1['Description'], autopct='%1.1f%%')
plt.title("JURIDICAL FORM") 
# plt.show()
st.pyplot(fig1)
st.markdown("#")
st.markdown("#")
st.markdown("#")
### Question 3

#query tables : Which percentage of the companies are which type of entreprise?
@st.cache(allow_output_mutation=True)
def get_data_enterprise_Q3():
        return pd.read_sql_query ('''
                               SELECT count(EnterpriseNumber), TypeOfEnterprise
                               FROM enterprise
                               Group by TypeOfEnterprise
                               ''', connection)
@st.cache(allow_output_mutation=True)
def get_data_code_Q3():
        return pd.read_sql_query ('''
                               SELECT *
                               FROM code
                               WHERE Language=="FR" AND Category=="TypeOfEnterprise"
                               ''', connection)

df_Q3T1 = get_data_enterprise_Q3()
df_Q3T1.rename(columns = {'TypeOfEnterprise':'Code'}, inplace = True)
df_Q3T2 = get_data_code_Q3()
#merge two df
df_Q3 = pd.merge(df_Q3T1, df_Q3T2, on='Code')
df_Q3 = df_Q3[["count(EnterpriseNumber)", "Description"]]


# Pie chart, where the slices will be ordered and plotted counter-clockwise:

labels = df_Q3["Description"]
sizes = df_Q3["count(EnterpriseNumber)"]

fig3, ax3 = plt.subplots()
ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("TYPE OF ENTERPRISE") 
st.pyplot(fig3)

st.markdown("#")
st.markdown("#")
st.markdown("#")

### QUESTION 4
#SQL query + df creating
@st.cache(allow_output_mutation=True)
def get_data_mapping():
        return pd.read_csv("mapping_sector_2008.csv")

# @st.cache(allow_output_mutation=True)
def get_data_enterprise_activity():
        return pd.read_sql_query ('''
                               SELECT EnterpriseNumber, StartDate, NaceCode
                               FROM enterprise
                               INNER JOIN activity ON enterprise.EnterpriseNumber = activity.EntityNumber
                               WHERE NaceVersion==2008
                               ''',connection)

#DATA CLEANING : 
# First two digit extract
df_Q4T1 = get_data_enterprise_activity()
df_Q4T1["NaceCode"] = df_Q4T1.NaceCode.str[:2].astype(int)
# Age caclulation
df_Q4T1['StartDate'] = pd.to_datetime(df_Q4T1['StartDate'])
df_Q4T1['StartDate'] = df_Q4T1['StartDate'].dt.year
today = datetime.today()
df_Q4T1['Age'] = today.year - df_Q4T1['StartDate']

#Create dictionnary from csv file
df_Q4M2008 = get_data_mapping()
df_Q4M2008.code_sector.astype(int)
dict_M2008 = df_Q4M2008.set_index('code_sector').to_dict()['title_sector']
#Do the mapping btw the df and the dictionary
df_Q4T1["sector"] = df_Q4T1["NaceCode"].map(dict_M2008)
#Create the new dataframe with grouping and average age per sector
df_Q4T1 = df_Q4T1.groupby("sector").agg({"Age":"mean"}).round(2).sort_values('Age', ascending=False).reset_index()

#GRAPH 4 --> need to finetune the graph with sector on Y axis + shorten the labels
st.write(f"<h1 style='text-align: center; color: black;'>ENTERPRISE AVERAGE AGE BY SECTOR</h0>", unsafe_allow_html=True)
fig, ax = plt.subplots()
ax.barh(df_Q4T1['sector'], df_Q4T1['Age'])
f = lambda x: textwrap.fill(x.get_text(), 75)
ax.set_yticklabels(map(f, ax.get_yticklabels()))
fig.set_size_inches(18.5, 15.5, forward=True)
# plt.title("ENTERPRISE AVERAGE AGE BY SECTOR",fontsize=20)
plt.xlabel('Age (Years)')
st.pyplot(fig)