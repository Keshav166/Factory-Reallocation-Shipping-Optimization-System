import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
recommendations = pd.read_csv(
    "factory_recommendations.csv"
)

df = pd.read_csv(
    "nassau_clustered.csv"
)

st.set_page_config(
    page_title="Factory Optimization System",
    layout="wide"
)

st.title("🍫 Factory Reallocation & Shipping Optimization System")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", len(df))
col2.metric("Total Products", df["Product Name"].nunique())
col3.metric("Total Factories", 5)
col4.metric("Recommendations", len(recommendations))

st.header("Factory Recommendations")

product = st.selectbox(
    "Select Product",
    recommendations["Product"]
)

result = recommendations[recommendations["Product"] == product]

if result.empty:
    st.warning("No data found for selected product")
    st.stop()
st.dataframe(result)
st.header("🏭 Orders by Factory")

factory_counts = df["Factory"].value_counts()

fig2, ax2 = plt.subplots()

ax2.bar(
    factory_counts.index.astype(str),
    factory_counts.values
)

ax2.set_title("Orders by Factory")
plt.xticks(rotation=45)

st.pyplot(fig2)
st.header("💰 Top Products by Profit")

profit_data = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots()

profit_data.plot(
    kind="bar",
    ax=ax3
)

plt.xticks(rotation=75)

st.pyplot(fig3)
st.header("🌎 Orders by Region")

region_counts = df["Region"].value_counts()

fig4, ax4 = plt.subplots()

ax4.bar(
    region_counts.index.astype(str),
    region_counts.values
)

st.pyplot(fig4)
st.header("🔮 What-If Scenario Analysis")

current_factory = result.iloc[0]["Current Factory"]
new_factory = result.iloc[0]["Alternative Factory"]

st.write(
    f"Current Factory: **{current_factory}**"
)

st.write(
    f"Recommended Factory: **{new_factory}**"
)
score = result.iloc[0]["Score"]

st.metric(
    "Optimization Score",
    f"{score:.2f}"
)
cluster_counts = df["Cluster"].value_counts()

fig, ax = plt.subplots()

ax.bar(
    cluster_counts.index.astype(str),
    cluster_counts.values
)

ax.set_title("Orders by Cluster")

st.pyplot(fig)
st.sidebar.title("Filters")

selected_product = st.sidebar.selectbox(
    "Select Product",
    recommendations["Product"]
)
if score >= 90:
    st.success("🟢 Low Risk Recommendation")
elif score >= 70:
    st.warning("🟡 Medium Risk Recommendation")
else:
    st.error("🔴 High Risk Recommendation")
col1, col2 = st.columns(2)

col1.info(f"Current Factory\n\n{current_factory}")
col2.success(f"Recommended Factory\n\n{new_factory}")
st.write("Optimization Confidence")

st.progress(min(int(score), 100))
