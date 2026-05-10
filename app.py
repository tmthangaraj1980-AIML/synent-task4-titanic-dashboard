import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="Titanic Dashboard",
    layout="wide"
)

# Title
st.title("🚢 Titanic Survival Dashboard")

st.markdown("Interactive dashboard for Titanic dataset analysis")

# Upload Dataset
uploaded_file = st.file_uploader(
    "Upload Titanic CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Sidebar
    st.sidebar.header("Filter Data")

    gender = st.sidebar.multiselect(
        "Select Gender",
        options=df["Sex"].unique(),
        default=df["Sex"].unique()
    )

    passenger_class = st.sidebar.multiselect(
        "Select Passenger Class",
        options=df['passenger_class'].unique(),
        default=df["passenger_class"].unique()
    )

    filtered_df = df[
        (df["Sex"].isin(gender)) &
        (df["passenger_class"].isin(passenger_class))
    ]

    # Metrics
    st.subheader("📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Passengers", filtered_df.shape[0])
    col2.metric("Average Age", round(filtered_df["Age"].mean(), 1))
    col3.metric(
        "Survival Rate",
        f"{round(filtered_df['survival_status'].mean()*100, 1)}%"
    )

    # Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(filtered_df.head())

    # Charts
    st.subheader("📊 Visualizations")

    # Survival Count
    fig1, ax1 = plt.subplots()

    sns.countplot(
        x='survival_status',
        data=filtered_df,
        ax=ax1
    )

    st.pyplot(fig1)

    # Gender Distribution
    fig2, ax2 = plt.subplots()

    filtered_df["Sex"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax2
    )

    st.pyplot(fig2)

    # Age Distribution
    fig3, ax3 = plt.subplots()

    sns.histplot(
        filtered_df["Age"],
        kde=True,
        ax=ax3
    )

    st.pyplot(fig3)

    # Correlation Heatmap
    st.subheader("🔥 Correlation Heatmap")

    fig4, ax4 = plt.subplots(figsize=(8, 5))

    sns.heatmap(
        filtered_df.corr(numeric_only=True),
        annot=True,
        cmap="coolwarm",
        ax=ax4
    )

    st.pyplot(fig4)

    # Missing values
    st.subheader("❌ Missing Values")

    st.write(filtered_df.isnull().sum())

else:
    st.info("Please upload a CSV file to continue.")