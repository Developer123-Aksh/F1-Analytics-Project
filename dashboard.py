import streamlit as st
import pandas as pd
import plotly.express as px

from race_simulator import simulate_race
from probability_engine import calculate_probabilities
from monte_carlo import simulate_multiple_races
from statistics_analysis import dataset_stats

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="F1 Analytics",
    layout="wide"
)

# ---------------- THEME ----------------
px.defaults.template = "plotly_dark"

st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0b0b0b, #141414);
    color: white;
}

/* Headers */
h1 {
    color: #E10600;
    font-weight: 700;
}
h2, h3 {
    color: #ffffff;
}

/* Metrics Cards */
[data-testid="stMetric"] {
    background: #1c1c1c;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #2a2a2a;
    transition: 0.3s;
}
[data-testid="stMetric"]:hover {
    border: 1px solid #E10600;
    transform: scale(1.03);
}

/* Buttons */
.stButton>button {
    background-color: #E10600;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #ff1e1e;
}

/* Tabs */
.stTabs [role="tab"] {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
# 🏎️ F1 PERFORMANCE DASHBOARD  
### *Speed • Data • Strategy*
""")

# ---------------- LOAD DATA ----------------
file_path = "F1Drivers_Dataset.csv"
df = pd.read_csv(file_path)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "🏁 Simulation", 
    "📈 Probabilities", 
    "🔍 Drivers"
])

# ================= OVERVIEW =================
with tab1:
    st.subheader("📊 Season Overview")

    stats = dataset_stats(file_path)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Drivers", stats.get("Total Drivers"))
    col2.metric("Active", stats.get("Active Drivers"))
    col3.metric("Champions", stats.get("Champions"))
    col4.metric("Race Wins", stats.get("Total Race Wins"))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        nationality_counts = df['Nationality'].value_counts().head(10)
        fig = px.bar(
            x=nationality_counts.index,
            y=nationality_counts.values,
            color_discrete_sequence=["#E10600"]
        )
        fig.update_layout(title="Top Nationalities")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        decade_counts = df['Decade'].value_counts().sort_index()
        fig = px.line(
            x=decade_counts.index.astype(str),
            y=decade_counts.values,
            markers=True
        )
        fig.update_layout(title="Drivers by Decade")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        top_winners = df.nlargest(10, 'Race_Wins')
        fig = px.bar(
            top_winners,
            x='Driver',
            y='Race_Wins',
            color_discrete_sequence=["#ff4d4d"]
        )
        fig.update_layout(title="🏆 Top Winners", xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        top_champions = df[df['Championships'] > 0].nlargest(10, 'Championships')
        fig = px.bar(
            top_champions,
            x='Driver',
            y='Championships',
            color_discrete_sequence=["#FFD700"]  # premium gold
        )
        fig.update_layout(title="🏆 Champions", xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

# ================= SIMULATION =================
with tab2:
    st.subheader("🏁 Race Simulation")

    if st.button("Run Race Simulation"):
        with st.spinner("Simulating race..."):
            race_results = simulate_race(file_path)

        st.success("Race Completed")

        col1, col2 = st.columns([2, 1])

        with col1:
            results_df = pd.DataFrame([
                {"Pos": i+1, "Driver": d.name, "Time": round(d.total_time, 2)}
                for i, d in enumerate(race_results[:20])
            ])
            st.dataframe(results_df, use_container_width=True)

        with col2:
            st.markdown("### 🏆 Podium")
            st.markdown(f"🥇 **{race_results[0].name}**")
            st.markdown(f"🥈 **{race_results[1].name}**")
            st.markdown(f"🥉 **{race_results[2].name}**")

# ================= PROBABILITIES =================
with tab3:
    st.subheader("📈 Win Probability")

    num_mc = st.slider("Simulations", 100, 10000, 3000)

    with st.spinner("Calculating probabilities..."):
        prob_df = calculate_probabilities(file_path)
        drivers = prob_df['Driver'].tolist()
        probs = prob_df['probability'].tolist()
        mc_results = simulate_multiple_races(drivers, probs, num_mc)

    mc_df = pd.DataFrame(sorted(mc_results.items(), key=lambda x: x[1], reverse=True),
                         columns=['Driver', 'Probability'])

    mc_df['Probability %'] = (mc_df['Probability'] * 100).round(2)

    col1, col2 = st.columns(2)

    with col1:
        top15 = mc_df.head(15)
        fig = px.bar(
            top15,
            x='Driver',
            y='Probability %',
            color_discrete_sequence=["#E10600"]
        )
        fig.update_layout(title="🏁 Championship Prediction", xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            top15,
            values='Probability %',
            names='Driver',
            hole=0.5
        )
        fig.update_layout(title="Probability Share")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(mc_df.head(20), use_container_width=True)

# ================= DRIVER EXPLORER =================
with tab4:
    st.subheader("🔍 Driver Explorer")

    search = st.text_input("Search Driver")

    filtered = df[df['Driver'].str.contains(search, case=False, na=False)] if search else df
    driver = st.selectbox("Select Driver", filtered['Driver'])

    if driver:
        d = df[df['Driver'] == driver].iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Wins", int(d['Race_Wins']))
        col2.metric("Podiums", int(d['Podiums']))
        col3.metric("Titles", int(d['Championships']))

        col4, col5, col6 = st.columns(3)
        col4.metric("Poles", int(d['Pole_Positions']))
        col5.metric("Fastest Laps", int(d['Fastest_Laps']))
        col6.metric("Points", d['Points'])

        metrics = ['Pole_Rate', 'Start_Rate', 'Win_Rate', 'Podium_Rate', 'FastLap_Rate']

        fig = px.bar(
            x=[m.replace('_', '') for m in metrics],
            y=[d[m]*100 for m in metrics],
            color_discrete_sequence=["#00C2FF"]
        )
        fig.update_layout(title="Performance Metrics (%)")
        st.plotly_chart(fig, use_container_width=True)

        st.json({
            "Nationality": d['Nationality'],
            "Active": "Yes" if d['Active'] else "No",
            "Decade": d['Decade']
        })