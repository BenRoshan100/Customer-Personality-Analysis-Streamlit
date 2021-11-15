#################
### LIBRARIES ###
#################
import streamlit as st 
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
matplotlib.use('Agg')
pd.set_option('display.max_columns', None)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
from PIL import Image

###Set Banner###
image = Image.open('customer_analysis.png')
st.image(image,use_column_width=True)

### Data Import ###
df_database = pd.read_csv("marketing_campaign.csv", sep="\t")
measure_types = ['sum','mean','median','max','min','count','std']
ed_types=['Graduation', 'PhD', 'Master', 'Basic', '2n Cycle']
marital_types=['Single', 'Together', 'Married', 'Divorced', 'Widow', 'Alone','Absurd', 'YOLO']
response_types=[0,1]
complain_types=[0,1]
visit_slider = [0,1,2,3,4,5,6,7,8,9,10]


#################
### SELECTION ###
#################

st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')
### YEAR OF BIRTH RANGE ###
st.sidebar.markdown("**First select the key demographics of the customers you want to analyze:** 👇")
unique_YOB = df_database.Year_Birth.unique()
sorted_YOB=sorted(unique_YOB)
try:
    start_YOB, end_YOB = st.sidebar.select_slider('Select the YOB range you want to include', sorted_YOB,value=[min(sorted_YOB),max(sorted_YOB)])
except TypeError:
    start_YOB, end_YOB=0,0

df_database = df_database[df_database['Year_Birth'].between(start_YOB, end_YOB)]


### INCOME RANGE ###
unique_income = df_database.Income.unique()
sorted_income=sorted(unique_income)
start_income,end_income = st.sidebar.select_slider('Select the Income range you want to include', sorted_income, value=[min(sorted_income),max(sorted_income)])

df_database = df_database[df_database['Income'].between(start_income, end_income)]

### KID RANGE ###
unique_kid = df_database.Kidhome.unique()
sorted_kid=sorted(unique_kid)
no_kid= st.sidebar.select_slider('Select the Kid at Home range you want to include', sorted_kid)
df_database = df_database[df_database.Kidhome==no_kid]

### TEEN RANGE ###
unique_teen = df_database.Teenhome.unique()
sorted_teen=sorted(unique_teen)
no_teen= st.sidebar.select_slider('Select the Teen at Home range you want to include', sorted_teen)
df_database = df_database[df_database.Teenhome==no_teen]

### RECENCY RANGE ###
unique_recency = df_database.Recency.unique()
sorted_recency=sorted(unique_recency)
start_recency,end_recency= st.sidebar.select_slider('Number of days since customer last purchase.', sorted_recency, value=[min(sorted_recency),max(sorted_recency)])
df_database = df_database[df_database['Recency'].between(start_recency, end_recency)]

###EDUCATIONAL QUALIFICATION###
all_ed_selected = st.sidebar.selectbox('Educational qualitifaction of the customers', ['Include all available educational qualifications','Select qualification manually (choose below)'])
if all_ed_selected == 'Select qualification manually (choose below)':
    customer_edqualification=st.sidebar.multiselect("Select and deselect the qualifications you would like to include in the analysis", ed_types)
    df_database = df_database[(df_database.Education.isin(customer_edqualification))]


### MARITAL STATUS ###
all_status_selected = st.sidebar.selectbox('Marital Status of the customers', ['Include all available marital status','Select status manually (choose below)'])
if all_status_selected == 'Select status manually (choose below)':
    customer_maritalstatus=st.sidebar.multiselect("Select and deselect the status you would like to include in the analysis", marital_types)
    df_database = df_database[(df_database.Marital_Status.isin(customer_maritalstatus))]

####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Customer Personality Analysis')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Ben Roshan](https://www.linkedin.com/in/benroshan100/)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("""There's a saying in business world,'Customers are always right !' Before creating a path to reach your product, 
			it is wise to understand what customer likes and dislikes about your solution. Marketing helps us to provide information about our product,
			and also to gather the feedback or reaction of customers. Understanding the customers you serve is crucial in this market. Here's a short analysis report
			of customer personality analysis in a marketing campaign""")
    st.markdown("You can find the source code in the [Ben Roshan GitHub Repository](https://github.com/BenRoshan100/Customer-Personality-Analysis-Streamlit)")



####################
#### DATAFRAME #####
####################
st.subheader('Overview of Data')
st.dataframe(df_database.head(50))

####################
#### FUNCTIONS #####
####################
# Campaign Plot function
def campaign_plot(response,measure):
	# Pivoted marketing_campaign_csv into df2
	global df2
	unused_columns = df_database.columns.difference(set(['Response']).union(set([])).union(set({'AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4','AcceptedCmp5'})))
	tmp_df = df_database.drop(unused_columns, axis=1)
	pivot_table = tmp_df.pivot_table(
    	index=['Response'],
    	values=['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4','AcceptedCmp5'],
    	aggfunc={'AcceptedCmp1': [measure], 'AcceptedCmp2': [measure], 'AcceptedCmp3': [measure], 'AcceptedCmp4': [measure],'AcceptedCmp5': [measure]}
	)

	# Reset the column name and the indexes
	df2 = pivot_table.reset_index()
	df2 = pivot_table.droplevel(axis=1, level=1).reset_index()
	fig = go.Figure()
	
	df2 = df2.loc[df2.Response == response]
	# Add the bar chart traces to the graph
	for column_header in ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4','AcceptedCmp5']:
		fig.add_trace(
			go.Bar( 
			x=df2['Response'],
			y=df2[column_header],
            name=column_header
            )
		)
	fig.update_layout(
		xaxis_title='Response',
        yaxis_title='',
        title='Campaign Results',
        barmode='group',
    )
	fig.show(renderer="iframe")
	st.plotly_chart(fig)


# Products Plot function
def product_plot(complain,measure):
	# Pivoted marketing_campaign_csv into df2
	global df2
	unused_columns = df_database.columns.difference(set(['Complain']).union(set([])).union(set({'MntFishProducts', 'MntMeatProducts', 'MntFruits','MntWines','MntSweetProducts', 'MntGoldProds'})))
	tmp_df = df_database.drop(unused_columns, axis=1)
	pivot_table = tmp_df.pivot_table(
    	index=['Complain'],
    	values=['MntFishProducts', 'MntMeatProducts', 'MntFruits','MntWines','MntSweetProducts', 'MntGoldProds'],
    	aggfunc={'MntFishProducts': [measure], 'MntMeatProducts': [measure], 'MntFruits': [measure], 'MntWines': [measure],'MntSweetProducts': [measure],'MntGoldProds': [measure]}
	)

	# Reset the column name and the indexes
	df2 = pivot_table.reset_index()
	df2 = pivot_table.droplevel(axis=1, level=1).reset_index()
	fig = go.Figure()
	
	df2 = df2.loc[df2.Complain == complain]
	# Add the bar chart traces to the graph
	for column_header in ['MntFishProducts', 'MntMeatProducts', 'MntFruits','MntWines','MntSweetProducts', 'MntGoldProds']:
		fig.add_trace(
			go.Bar( 
			x=df2['Complain'],
			y=df2[column_header],
            name=column_header
            )
		)
	fig.update_layout(
		xaxis_title='Complain',
        yaxis_title='',
        title='Product Sales',
        barmode='group',
    )
	fig.show(renderer="iframe")
	st.plotly_chart(fig)

# Purchase function
def purchase_plot(measure):
	# Pivoted marketing_campaign_csv into df2
	global df2
	unused_columns = df_database.columns.difference(set(['NumWebVisitsMonth']).union(set([])).union(set({'NumWebPurchases', 'NumStorePurchases', 'NumDealsPurchases', 'NumCatalogPurchases'})))
	tmp_df = df_database.drop(unused_columns, axis=1)
	pivot_table = tmp_df.pivot_table(
    	index=['NumWebVisitsMonth'],
    	values=['NumWebPurchases', 'NumStorePurchases', 'NumDealsPurchases', 'NumCatalogPurchases'],
    	aggfunc={'NumWebPurchases': [measure], 'NumStorePurchases': [measure], 'NumDealsPurchases': [measure], 'NumCatalogPurchases': [measure]}
	)

	# Reset the column name and the indexes
	df2 = pivot_table.reset_index()
	df2 = pivot_table.droplevel(axis=1, level=1).reset_index()
	fig = go.Figure()
	
	#df2 = df2.loc[df2.NumWebVisitsMonth == visits]
	# Add the bar chart traces to the graph
	for column_header in ['NumWebPurchases', 'NumStorePurchases', 'NumDealsPurchases', 'NumCatalogPurchases']:
		fig.add_trace(
			go.Scatter( 
			x=df2['NumWebVisitsMonth'],
			y=df2[column_header],
			mode='markers',
            name=column_header
            )
		)
		fig.update_layout(
			xaxis_title='NumWebVisitsMonth',
			yaxis_title='',
			title='Number of Visits per month Vs Medium of purchase',
			barmode='group',
			)
	fig.show(renderer="iframe")
	st.plotly_chart(fig)


########################################
#### CAMPAIGN RESULTS ####
########################################
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .1))
with row4_1:
    st.subheader('Analysis by Campaign Results')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row5_1:
    st.markdown('Investigate a variety of stats for each response types. Which campaign had a major impact on the response of customers?')
    plot_x_per_response = st.selectbox ("Which Response do you want to select ?Response:0-Negative, 1-Positive",response_types)
    plot_x_per_measure = st.selectbox ("Which measure do you want to analyze?",measure_types)
with row5_2:
	campaign_plot(plot_x_per_response,plot_x_per_measure)



##################################################
#### ANALYSIS BY PRODUCT SALES AND COMPLAINTS ####
##################################################
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Analysis by Sales and Complaints')
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row7_1:
    st.markdown('Investigate a variety of stats for each response types. Which product sales has been impacted by complaints?')
    plot_x_per_complain = st.selectbox ("Complain:0-No Complaints, 1-Complaint reistered",complain_types)
    plot_x_per_stat = st.selectbox ("Which stats do you want to analyze?",measure_types)
with row7_2:
	product_plot(plot_x_per_complain,plot_x_per_stat)


##################################################
#### ANALYSIS BY PRODUCT SALES AND COMPLAINTS ####
##################################################
row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
with row8_1:
    st.subheader('Relation between Number of visits and channels for purchase')
row9_spacer1, row9_1, row9_spacer2, row9_2, row9_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row9_1:
    st.markdown('Investigate a variety of stats for each response types. Is there any relation between number of website visits and purchase channels')
    #plot_x_per_visit = st.select_slider ("Select the Number of website visits",visit_slider)
    plot_x_per_stat = st.selectbox ("Which stats do you want to measure?",measure_types)
with row9_2:
	purchase_plot(plot_x_per_stat)
