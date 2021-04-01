import streamlit as st
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime as dt
import datetime


st.sidebar.title('Mortal Kombat 11: P&L Detail')
st.sidebar.subheader('July 2020\nRelease: April 2019')
# st.sidesubheader('Release: April 2019')
# st.sidebar.subheader('Property Options')



## Step - 1 Inputs

## Mandatory Inputs
st.markdown(""" 
# Input Parameters (Default) 
""")
params={
'total_units' : st.sidebar.number_input("Total Units (K):",value=7626.288,min_value=100.0,max_value=100000.0,step=1.0,format="%.3f") ,
'physical_ratio' : st.sidebar.slider("Physical Digital Ratio (%):", value = 62.5739853,min_value=0.0,max_value=100.0,step = 0.01,format="%.3f"),
'digital_asp' : st.sidebar.slider("Digital ASP ($):",min_value=0.0,max_value=120.0, value = 35.4891899183981,step = 0.01,format="%.3f") ,
'physical_asp' : st.sidebar.slider("Physical ASP ($):",min_value=0.0,max_value=120.0, value = 32.7142184714979,step = 0.01,format="%.3f"),
'arpun': st.sidebar.slider("ARPUN ($):",min_value=0.0,max_value=100.0, value = 6.25523373239221,step = 0.01,format="%.3f")
}


total_units = params['total_units']
physical_ratio =params['physical_ratio']
digital_asp = params['digital_asp']
physical_asp = params['physical_asp']
arpun = params['arpun']

a,b,c = st.beta_columns(3)
d,e = st.beta_columns(2)


anciliary=a.number_input("Ancilliary Dev ($ M):", value= 9.4929112285702,format="%.3f")
price_protection_ratio=b.number_input("Price Protection ($) /unit:", value = -3.8785529574475,format="%.3f")
product_placement_ratio=c.number_input("Product Placement ($) /unit:", value = -2.98731229332019,format="%.3f")


## Step - 1 Outputs 

digital_units = (1-(physical_ratio/100.0) )*total_units
physical_units = (physical_ratio/100.0)*total_units
price_protection = price_protection_ratio*physical_units/1000.0
product_placement = product_placement_ratio*physical_units/1000.0
gross_revenue_physical = (physical_asp*physical_units/1000.0) - price_protection - product_placement
net_revenue_physical = gross_revenue_physical + price_protection + product_placement
net_revenue_digital = digital_asp*digital_units/1000.0
gross_revenue_digital = net_revenue_digital/0.7
net_revenue_live = arpun*total_units/1000.0
gross_revenue_live = net_revenue_live/0.7
gross_revenue_total = gross_revenue_digital+gross_revenue_physical+gross_revenue_live+anciliary
net_revenue_total = net_revenue_digital+net_revenue_physical+net_revenue_live + anciliary 


df1 = pd.DataFrame(columns=['Physical', 'Digital', 'Live', 'Total'])
df1 = df1.append(pd.DataFrame(data=[[float(format(physical_units, '.0f')),float(format(digital_units, '.0f')), '-', float(format(total_units, '.0f'))]],columns=['Physical', 'Digital', 'Live', 'Total']))
df1 = df1.append(pd.DataFrame(data=[[float(format(physical_asp, '.2f')),float(format(digital_asp, '.2f')), '-', '-']],columns=['Physical', 'Digital', 'Live', 'Total']))
df1 = df1.append(pd.DataFrame(data=[['-','-', float(format(arpun, '.2f')), '-']],columns=['Physical', 'Digital', 'Live', 'Total']))

df1 = df1.append(pd.DataFrame(data=[[float(format(gross_revenue_physical, '.2f')),float(format(gross_revenue_digital, '.2f')), '-', float(format(gross_revenue_total, '.2f'))]],columns=['Physical', 'Digital', 'Live', 'Total']))
df1 = df1.append(pd.DataFrame(data=[[float(format(net_revenue_physical, '.2f')),float(format(net_revenue_digital, '.2f')), float(format(net_revenue_live, '.2f')), float(format(net_revenue_total, '.2f'))]],columns=['Physical', 'Digital', 'Live', 'Total']))
df1.index = ['Units (K)','Avg. Net Price ($)','ARPUN ($)', 'Gross Revenue ($ M)', 'Net Revenue ($ M)' ]





## Step -2 Inputs

cost_of_product = st.sidebar.number_input("Cost of Product/unit ($):", value = 10.8046996885165, min_value = 0.0, max_value = 120.0,step = 0.1, format="%.2f" )
cost_of_hosting = st.sidebar.number_input("Cost of Hosting/unit ($):", value = 0.368101932, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")
cost_of_customer_service = st.sidebar.number_input("Cost of Customer Service/unit ($):", value = 0.03281675, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")
cost_of_live_dev = st.sidebar.number_input("Cost of Live Development/unit ($):", value=1.339877906, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")
cost_of_platform = st.sidebar.number_input("Cost of Platform/unit ($):", value = 0.282137627, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")
cost_of_digital_publishing = st.sidebar.number_input("Cost of Digital Publishing/unit ($):", value = 0.222797097, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")
cost_of_freight = st.sidebar.number_input("Cost of Freight/unit ($):", value = 0.223461122, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")
cost_of_other = st.sidebar.number_input("Other Costs/unit ($):", value = 0.075046866, min_value = 0.0, max_value = 120.0,step = 0.01, format="%.2f")

## Step -2 Outputs

total_cost_of_revenue = (cost_of_product*physical_units+ total_units*(cost_of_customer_service+cost_of_digital_publishing+cost_of_freight+cost_of_hosting+cost_of_live_dev+cost_of_other+cost_of_platform))/1000


## Step -3 Inputs

ua_marketing = d.slider("UA Marketing (% Net Revenue):", value=3.9949628611929,min_value=0.0,max_value=100.0,step = 0.01,format="%.3f")
consumer_marketing = e.slider("Consumer Marketing (% Net Revenue):", value = 11.328198291782,min_value=0.0,max_value=100.0,step = 0.01,format="%.3f")

## Step -3 Outputs

marketing_cost = ua_marketing*net_revenue_total/100 + consumer_marketing*net_revenue_total/100
variable_contribution = net_revenue_total - total_cost_of_revenue - marketing_cost





## Step -4 Inputs

production_cost = st.number_input("Production Cost ($ M):",value=93.317372113312,format="%.3f")

## Step -5 Inputs

internal_ip_perc = a.slider("Internal IP (% Net Revenue):",value=12.4770674479954,min_value=0.0,max_value=100.0,step = 0.01,format="%.3f")
external_ip_perc = b.slider("External IP (% Net Revenue):",value=1.55403935311131,min_value=0.0,max_value=100.0,step = 0.01,format="%.3f")
developer_perc = c.slider("Developer cost (% Net Revenue):",value =0.629408249777735,min_value=0.0,max_value=100.0,step = 0.01,format="%.3f")

## Step -5 Outputs

internal_ip = internal_ip_perc*net_revenue_total/100.0
external_ip= external_ip_perc*net_revenue_total/100.0
developer = developer_perc*net_revenue_total/100.0


operating_contribution_before_ic = variable_contribution - production_cost -external_ip - developer
operating_contribution_after_ic = operating_contribution_before_ic - internal_ip

operating_income_of_net_revenue_perc = (operating_contribution_before_ic*100.0)/net_revenue_total
operating_income_of_net_revenue_perc = float(format(operating_income_of_net_revenue_perc, '.2f'))

operating_income_of_total_cost_perc = (operating_contribution_before_ic*100.0)/(net_revenue_total-operating_contribution_before_ic)
operating_income_of_total_cost_perc = float(format(operating_income_of_total_cost_perc, '.2f'))
total_cost_of_revenue = float(format(total_cost_of_revenue, '.2f'))
marketing_cost = float(format(marketing_cost, '.2f'))
variable_contribution = float(format(variable_contribution, '.2f'))
internal_ip = float(format(internal_ip, '.2f'))
external_ip = float(format(external_ip, '.2f'))
developer = float(format(developer, '.2f'))

operating_contribution_before_ic = float(format(operating_contribution_before_ic, '.2f'))
operating_contribution_after_ic = float(format(operating_contribution_after_ic, '.2f'))



participtions = external_ip + internal_ip + developer




st.markdown(""" <style>h1{color: white ; font-family: "Garamond"}
</style> 
#  Mortal Kombat 11 Ultimate - 2 Years P&L Calculations  

""",True)  


st.write(df1)
st.write(""" _ The Total Cost of Revenue ($ M): _""",total_cost_of_revenue)
st.write(""" _ Marketing Cost ($ M): _""",marketing_cost)
st.write(""" _ Variable Contribution ($ M): _""",variable_contribution)  

st.write(""" _ Internal IP ($ M): _""",internal_ip)  
st.write(""" _ External IP ($ M): _""",external_ip)  
st.write(""" _ Total Participations ($ M): _""",participtions)  

st.write(""" _ Operating Contribution before IC Parts ($ M): _""",operating_contribution_before_ic)  
st.write(""" _ Operating Contribution after IC Parts ($ M): _""",operating_contribution_after_ic)  

st.write(""" _ The Operating Income as Net Revenue (%): _""",operating_income_of_net_revenue_perc)
st.write(""" _ The Operating Income as Total Cost (%): _""",operating_income_of_total_cost_perc)












