import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("hotel_bookings.csv")

df1=pd.read_csv("hotel_bookings.csv",usecols=[3,4,6,7,8,26,27])

months = {'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06','July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}

df1['arrival_date_month'] = df['arrival_date_month'].apply(lambda x: months[x])

df1['arrival_date_month']=pd.to_numeric(df1.arrival_date_month)
df1['date']=pd.to_datetime((df1.arrival_date_year*10000+df1.arrival_date_month*100+df1.arrival_date_day_of_month).apply(str),format='%Y%m%d')
df1['weekdays']=df1['date'].dt.day_name()
df1=df1.drop(['arrival_date_year',
       'arrival_date_month',
       'arrival_date_day_of_month'],axis=1)
weekday_names=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday_counts=df1.groupby("weekdays").mean()
weekday_counts=weekday_counts.loc[weekday_names]

plt.figure(figsize=(8, 5))
plt.bar(weekday_names,weekday_counts['adr'],color=(0.3, 0.7, 0.6, 0.6))
plt.title('ADR per day',fontweight="bold", size=20)
plt.xlabel('Days', fontsize=14)
plt.ylabel('ADR', fontsize=14)
plt.savefig('static/adrPerday.jpg',bbox_inches = 'tight')

stay={'weekend':df1.stays_in_weekend_nights.mean(),'weekdays':df1.stays_in_week_nights.mean()}
keys = stay.keys()
values = stay.values()
plt.figure(figsize=(4, 3))
plt.bar(keys, values,color=(0.5, 0.4, 0.6, 0.6),width=[0.3,0.3],ec="black",align='center')
plt.title('Stays vs week time',fontweight="bold", size=15)
plt.xlabel('Days', fontsize=10)
plt.ylabel('Night Stays', fontsize=10)
plt.savefig('static/nightStayed.jpg',bbox_inches = 'tight')


plt.figure(figsize=(12, 6))
sns.countplot(x='hotel', data=df,palette='Pastel1')
plt.title("Cancelation rates in the Hotel",fontweight="bold", size=20)
plt.savefig('static/cancellation.jpg',bbox_inches = 'tight')

plt.figure(figsize=(8, 6))
sns.countplot(x='customer_type', data=df,palette='Pastel2',ec='black')
plt.title("Customer types",fontweight="bold", size=20)
plt.savefig('static/customers.jpg',bbox_inches = 'tight')


plt.figure(figsize=(12,6))
sns.lineplot(x='arrival_date_month', y='adr',  data= df)
plt.title("ADR wrt Month",fontweight="bold", size=20)
plt.savefig('static/adrPerMonth.jpg',bbox_inches = 'tight')

