import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper Function
def create_daily_rental_df(df):
    daily_rental_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered" : "sum",
        "cnt" : "sum"
    })
    daily_rental_df = daily_rental_df.reset_index()
    daily_rental_df.rename(columns={
        "casual": "count_user_casual",
        "registered" : "count_user_registered",
        "cnt" : "count_user_total"
    }, inplace=True)
    
    return daily_rental_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "total_rental_bikes"
    }, inplace=True)
    
    return byseason_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    byweathersit_df.rename(columns={
        "cnt": "total_rental_bikes"
    }, inplace=True)
    
    return byweathersit_df

# Load Data
day_df = pd.read_csv("./dashboard/day.csv", delimiter=",")
datetime_columns = ["dteday"]
day_df.sort_values(by = "dteday", inplace = True)
day_df.reset_index(inplace = True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    
    if min_date == max_date:
        start_date = min_date
        end_date = max_date
    else:
        # Mengambil start_date & end_date dari date_input
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]


# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_rental_df = create_daily_rental_df(main_df)
byseason_df = create_byseason_df(main_df)
byweathersit_df = create_byweathersit_df(main_df)

# plot number of daily rental (2011)
st.header('Dashboard 🚲')
st.subheader('Daily Bike Rental')

col1, col2, col3 = st.columns(3)

with col1 : 
    total_rentals = daily_rental_df.count_user_total.sum()
    st.metric("Total Bike Rentals Users", value = total_rentals)
    
with col2 :
    total_casual = daily_rental_df.count_user_casual.sum()
    st.metric("Total Bike Rental Casual Users", value = total_casual)
    
with col3 :
    total_registered = daily_rental_df.count_user_registered.sum()
    st.metric("Total Bike Rental Registered Users", value = total_registered)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rental_df["dteday"],
    daily_rental_df["count_user_total"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.grid()
ax.set_title("Total for Bike Sharing", fontsize = 25)

st.pyplot(fig)

# Demography
st.subheader("Bike Rental Demographic")

col1,col2 = st.columns(2)

colors = ["orange", "blue", "red", "purple"]
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        y="total_rental_bikes", 
        x="season",
        data=byseason_df.sort_values(by="total_rental_bikes", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total of Bike Rental Users by Season ", loc="center", fontsize=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    st.pyplot(fig)


with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        y="total_rental_bikes", 
        x="weathersit",
        data=byweathersit_df.sort_values(by="total_rental_bikes", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Total of Bike Rental Users by Weather Situation ", loc="center", fontsize=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    ax.set_xticklabels(["Clear", "Mist", "Light Snow"])
    st.pyplot(fig)    