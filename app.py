import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(
    page_title="Customer Behavior Dashboard",
    layout="wide"
)

# Title

st.title("🛒 Customer Behavior Dashboard")


# Load Data

df = pd.read_csv("customer_shopping_behavior.csv")

# age_groups

labels = [
    "Young adults",
    "Adult",
    "Middle-aged",
    "Senior"
]

df["age_group"] = pd.qcut(
    df["Age"],
    q=4,
    labels=labels
)

# Sidebar

st.sidebar.header("Filter")

subscription = st.sidebar.multiselect(
    "Subscription Status",
    options=df["Subscription Status"].unique(),
    default=df["Subscription Status"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

df = df[
    (df["Subscription Status"].isin(subscription)) &
    (df["Gender"].isin(gender)) &
    (df["Category"].isin(category))
]

# KPIs

st.subheader("KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Customers", f"{len(df):,}")

with col2:
    st.metric(
        "Average Purchase",
        f"{df['Purchase Amount (USD)'].mean():.2f} $"
    )

with col3:
    st.metric(
        "Average Rating",
        round(df["Review Rating"].mean(), 2)
    )

# TOP CHARTS

left, middle, right = st.columns(3)

# ---------------- Donut ----------------

with left:

    fig = px.pie(
        df,
        names="Subscription Status",
        hole=0.65,
        color="Subscription Status",
        color_discrete_map={
            "Yes": "#d65db1",
            "No": "#2b2bb2"
        }
    )

    fig.update_layout(
        title="Customers by Subscription",
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ---------------- Revenue ----------------

with middle:

    revenue = (
        df.groupby("Category")["Purchase Amount (USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue,
        x="Category",
        y="Purchase Amount (USD)",
        color_discrete_sequence=["#2b2bb2"]
    )

    fig.update_layout(
        title="Revenue by Category",
        height=350,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ---------------- Sales ----------------

with right:

    sales = (
        df.groupby("Category")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Sales")
    )

    fig = px.bar(
        sales,
        x="Category",
        y="Sales",
        color_discrete_sequence=["#2b2bb2"]
    )

    fig.update_layout(
        title="Sales by Category",
        height=350,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# BOTTOM CHARTS


bottom_left, bottom_right = st.columns(2)

# -------- Revenue by Age --------

with bottom_left:

    revenue = (
        df.groupby("age_group")["Purchase Amount (USD)"]
        .sum()
        .reset_index()
    )

    revenue["age_group"] = pd.Categorical(
        revenue["age_group"],
        categories=[
            "Young adults",
            "Middle-aged",
            "Adult",
            "Senior"
        ],
        ordered=True
    )

    revenue = revenue.sort_values("age_group")

    fig = px.bar(
        revenue,
        x="Purchase Amount (USD)",
        y="age_group",
        orientation="h",
        color_discrete_sequence=["#2b2bb2"]
    )

    fig.update_layout(
        title="Revenue by Age Group",
        height=350,
        showlegend=False,
        xaxis_title="",
        yaxis_title=""
    )

    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# -------- Sales by Age --------

with bottom_right:

    sales_age = (
        df.groupby("age_group")
        .size()
        .reset_index(name="Sales")
    )

    sales_age["age_group"] = pd.Categorical(
        sales_age["age_group"],
        categories=[
            "Young adults",
            "Middle-aged",
            "Senior",
            "Adult"
        ],
        ordered=True
    )

    sales_age = sales_age.sort_values("age_group")

    fig = px.bar(
        sales_age,
        x="Sales",
        y="age_group",
        orientation="h",
        color_discrete_sequence=["#2b2bb2"]
    )

    fig.update_layout(
        title="Sales by Age Group",
        height=350,
        showlegend=False,
        xaxis_title="",
        yaxis_title=""
    )

    
    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )