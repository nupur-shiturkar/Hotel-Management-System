import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("hotel_bookings.csv")

plt.figure(figsize=(12, 6))

sns.countplot(x='hotel',hue='is_canceled', data=df,palette='Pastel1')
plt.title("Cancelation rates in City hotel and Resort hotel",fontweight="bold", size=20)