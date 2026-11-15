from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="The Match Lab | Speed Dating, in Data",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).parent / "speed_dating.csv"
PREFERENCES = {
    "pref_o_attractive": "Attractiveness",
    "pref_o_sincere": "Sincerity",
    "pref_o_intelligence": "Intelligence",
    "pref_o_funny": "Humor",
    "pref_o_ambitious": "Ambition",
    "pref_o_shared_interests": "Shared interests",
}
TRAIT_RATING_COLUMNS = {
    "Attractiveness": "attractive_o",
    "Sincerity": "sinsere_o",
    "Intelligence": "intelligence_o",
    "Humor": "funny_o",
    "Ambition": "ambitous_o",
    "Shared interests": "shared_interests_o",
}


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, low_memory=False)
    data["age"] = pd.to_numeric(data["age"], errors="coerce")
    data["match"] = pd.to_numeric(data["match"], errors="coerce")
    data["decision"] = pd.to_numeric(data["decision"], errors="coerce")
    data["decision_o"] = pd.to_numeric(data["decision_o"], errors="coerce")
    data["wave"] = pd.to_numeric(data["wave"], errors="coerce")
    for column in [*TRAIT_RATING_COLUMNS.values(), "like", *PREFERENCES]:
        if column in data:
            data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=["match", "age", "gender"]).copy()
    data["match"] = data["match"].astype(int)
    data["gender_label"] = data["gender"].astype(str).str.capitalize()
    return data


def percent(value):
    return f"{value:.1%}"


data = load_data()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    :root { --ink:#202522; --muted:#757b75; --paper:#f8f7f3; --coral:#ef765f; --sage:#8f9e89; }
    .stApp { background: var(--paper); color: var(--ink); }
    .block-container { max-width: 1320px; padding-top: 2.1rem; padding-bottom: 4rem; }
    h1,h2,h3 { font-family:'Playfair Display', Georgia, serif !important; letter-spacing:-.025em; color:var(--ink); }
    p, label, div[data-testid="stMarkdownContainer"] { font-family:'DM Sans', sans-serif; }
    .hero { padding: 2.5rem 2.7rem 2.3rem; border-radius: 24px; background: #222925; color: #f8f7f3; margin: .3rem 0 1.6rem; position:relative; overflow:hidden; }
    .hero:after { content:'♡'; position:absolute; right:7%; top:-55px; font-size:250px; line-height:1; color:rgba(239,118,95,.12); font-family:Georgia,serif; }
    .eyebrow { text-transform:uppercase; letter-spacing:.16em; font:600 11px 'DM Sans',sans-serif; color:#f6a08e; margin-bottom:13px; }
    .hero h1 { color:#fffaf3 !important; font-size:clamp(2.4rem,5vw,4.4rem); line-height:1.02; margin:0; position:relative; z-index:1; }
    .hero p { color:#d5d9d3; font-size:1.05rem; max-width:720px; line-height:1.65; margin:.9rem 0 0; position:relative; z-index:1; }
    .section-kicker { color:#c46250; text-transform:uppercase; letter-spacing:.13em; font:700 11px 'DM Sans',sans-serif; margin:1.3rem 0 .45rem; }
    .note { background:#efeee7; border-left:3px solid #ef765f; padding:14px 17px; border-radius:4px 12px 12px 4px; color:#4c524d; font-size:.92rem; }
    .stMetric { background:#fffefa; border:1px solid #e9e6dc; border-radius:16px; padding:17px 19px; }
    div[data-testid="stMetricLabel"] p { color:#747970; }
    div[data-testid="stMetricValue"] { color:#252a26; }
    div[data-testid="stTabs"] button { font-weight:600; }
    section[data-testid="stSidebar"] { background:#eeede6; }
    .source { color:#737971; font-size:.82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">A data story about first impressions</div>
      <h1>The Match Lab</h1>
      <p>What makes two people want to meet again? Explore thousands of real speed dates and see how stated preferences, first impressions, and mutual interest line up.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Explore the study")
    st.caption("Use the filters to focus the records shown across the dashboard.")
    genders = sorted(data["gender_label"].dropna().unique().tolist())
    selected_genders = st.multiselect("Participant gender", genders, default=genders)
    age_min = int(data["age"].min())
    age_max = int(data["age"].max())
    age_range = st.slider("Participant age", age_min, age_max, (age_min, age_max))
    wave_min = int(data["wave"].min())
    wave_max = int(data["wave"].max())
    wave_range = st.slider("Study wave", wave_min, wave_max, (wave_min, wave_max))
    st.divider()
    st.markdown("**What counts as a match?**")
    st.caption("A match means both people said they wanted to see each other again.")

filtered = data[
    data["gender_label"].isin(selected_genders)
    & data["age"].between(age_range[0], age_range[1])
    & data["wave"].between(wave_range[0], wave_range[1])
].copy()

match_rate = filtered["match"].mean() if len(filtered) else 0
total_dates = len(filtered)
unique_events = filtered["wave"].nunique()
mutual_matches = int(filtered["match"].sum())

k1, k2, k3, k4 = st.columns(4)
k1.metric("Speed dates", f"{total_dates:,}")
k2.metric("Mutual matches", f"{mutual_matches:,}")
k3.metric("Match rate", percent(match_rate))
k4.metric("Study waves", f"{unique_events:,}")

st.markdown('<div class="section-kicker">Choose a question</div>', unsafe_allow_html=True)
overview_tab, preferences_tab, scenario_tab, about_tab = st.tabs(
    ["The big picture", "Preferences vs. reality", "Try a scenario", "About the data"]
)

with overview_tab:
    st.header("What seems to go with a match?")
    st.write("Mutual interest is rare enough to be interesting. Explore the pattern across first-date impressions and how often each person said yes.")
    left, right = st.columns([1.05, 1])
    with left:
        st.subheader("Match rate by overall liking")
        temp = filtered[["like", "match"]].dropna().copy()
        temp["Liking score"] = temp["like"].round().clip(1, 10).astype(int)
        liking = temp.groupby("Liking score", as_index=False).agg(
            match_rate=("match", "mean"), dates=("match", "size")
        )
        if not liking.empty:
            fig = px.line(
                liking,
                x="Liking score",
                y="match_rate",
                markers=True,
                custom_data=["dates"],
                color_discrete_sequence=["#e8755e"],
            )
            fig.update_traces(hovertemplate="Liking: %{x}<br>Mutual match rate: %{y:.1%}<br>Dates: %{customdata[0]}<extra></extra>", line=dict(width=3))
            fig.update_layout(yaxis_tickformat=".0%", xaxis=dict(dtick=1, title="Participant’s overall liking score"), yaxis_title="Share ending in mutual match", margin=dict(l=5,r=10,t=15,b=5), height=360, plot_bgcolor="#fffefa", paper_bgcolor="#fffefa")
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("There are no liking scores in this filtered sample.")
    with right:
        st.subheader("One-sided yes vs. mutual yes")
        decision_counts = filtered[["decision", "decision_o", "match"]].dropna()
        if not decision_counts.empty:
            decision_counts["Outcome"] = decision_counts.apply(
                lambda r: "Both said yes" if r["match"] == 1 else ("Participant said yes" if r["decision"] == 1 else ("Partner said yes" if r["decision_o"] == 1 else "Neither said yes")), axis=1
            )
            outcome = decision_counts["Outcome"].value_counts().rename_axis("Outcome").reset_index(name="Dates")
            order = ["Both said yes", "Participant said yes", "Partner said yes", "Neither said yes"]
            outcome["Outcome"] = pd.Categorical(outcome["Outcome"], categories=order, ordered=True)
            outcome = outcome.sort_values("Outcome")
            fig = px.bar(outcome, x="Dates", y="Outcome", orientation="h", text="Dates", color="Outcome", color_discrete_map={"Both said yes":"#e8755e", "Participant said yes":"#d8a28e", "Partner said yes":"#8f9e89", "Neither said yes":"#d8d8cf"})
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(showlegend=False, xaxis_title="Number of dates", yaxis_title="", margin=dict(l=5,r=30,t=15,b=5), height=360, plot_bgcolor="#fffefa", paper_bgcolor="#fffefa")
            st.plotly_chart(fig, width="stretch")
    st.markdown('<div class="note"><b>Read it carefully:</b> these are associations in one historical student speed-dating study. They do not show that any single trait causes a match.</div>', unsafe_allow_html=True)

with preferences_tab:
    st.header("What people say they want—and what gets noticed")
    st.write("Participants rated how important different qualities were in a partner. They also rated the person they met. Compare stated importance with average partner ratings among mutual matches and non-matches.")
    preference_values = filtered[list(PREFERENCES)].mean(numeric_only=True)
    pref_frame = pd.DataFrame({"Quality": list(PREFERENCES.values()), "Stated importance": [preference_values[c] for c in PREFERENCES]})
    rating_rows = []
    for label, column in TRAIT_RATING_COLUMNS.items():
        if column in filtered:
            for match_value, group_name in [(0, "No mutual match"), (1, "Mutual match")]:
                rating_rows.append({"Quality": label, "Outcome": group_name, "Average rating": filtered.loc[filtered["match"] == match_value, column].mean()})
    rating_frame = pd.DataFrame(rating_rows)
    left, right = st.columns(2)
    with left:
        st.subheader("Qualities people say matter")
        fig = px.bar(pref_frame.sort_values("Stated importance"), x="Stated importance", y="Quality", orientation="h", color="Stated importance", color_continuous_scale=["#e7d9c8", "#e8755e"])
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Average importance (0–100%)", yaxis_title="", margin=dict(l=5,r=5,t=15,b=5), height=400, plot_bgcolor="#fffefa", paper_bgcolor="#fffefa")
        st.plotly_chart(fig, width="stretch")
    with right:
        st.subheader("Average ratings on the date")
        fig = px.bar(rating_frame, x="Average rating", y="Quality", color="Outcome", barmode="group", orientation="h", color_discrete_map={"No mutual match":"#aab0a5", "Mutual match":"#e8755e"})
        fig.update_layout(xaxis_title="Average partner rating (1–10)", yaxis_title="", legend_title="", margin=dict(l=5,r=5,t=15,b=5), height=400, plot_bgcolor="#fffefa", paper_bgcolor="#fffefa")
        st.plotly_chart(fig, width="stretch")
    st.caption("The left chart records pre-date stated preferences; the right charts ratings after meeting. These measures are related but not directly comparable.")

with scenario_tab:
    st.header("Build a ‘what if’ scenario")
    st.write("Choose minimum partner ratings for qualities you care about. The app will show the historical match rate for dates whose recorded ratings met those cutoffs.")
    st.caption("This is a descriptive comparison, not a personal prediction or dating recommendation.")
    c1, c2, c3 = st.columns(3)
    inputs = {}
    for i, trait in enumerate(TRAIT_RATING_COLUMNS):
        with [c1, c2, c3][i % 3]:
            inputs[trait] = st.slider(f"Minimum {trait.lower()} rating", 1, 10, 6, key=f"scenario_{trait}")
    required_traits = st.multiselect(
        "Include qualities in this scenario",
        list(TRAIT_RATING_COLUMNS),
        default=["Attractiveness", "Humor"],
    )
    if required_traits:
        required_columns = [TRAIT_RATING_COLUMNS[trait] for trait in required_traits]
        scenario = filtered.dropna(subset=required_columns).copy()
        meets = pd.Series(True, index=scenario.index)
        for trait in required_traits:
            column = TRAIT_RATING_COLUMNS[trait]
            meets &= scenario[column] >= inputs[trait]
        similar = scenario.loc[meets]
        if len(similar):
            scenario_rate = similar["match"].mean()
            baseline = scenario["match"].mean()
            a, b, c = st.columns(3)
            a.metric("Dates meeting your cutoffs", f"{len(similar):,}")
            b.metric("Match rate in that group", percent(scenario_rate))
            c.metric("Filtered-sample baseline", percent(baseline), delta=f"{(scenario_rate - baseline)*100:+.1f} percentage points")
            st.markdown('<div class="note">This describes past dates in the dataset that met your selected rating cutoffs. It cannot tell whether a real future date will be a match.</div>', unsafe_allow_html=True)
        else:
            st.info("No dates in the current filters met every selected cutoff. Try lowering a threshold or including fewer qualities.")
    else:
        st.info("Select one or more qualities to explore a scenario.")

with about_tab:
    st.header("A real experiment, with important limits")
    st.write("This dataset comes from speed-dating events run at Columbia University between 2002 and 2004. Participants met for short dates, rated each other, and recorded whether they wanted to meet again. One row represents one participant’s view of one date.")
    st.markdown("#### How this app handles the data")
    st.markdown("- Converts outcome, age, wave, and rating fields to numeric types where possible.\n- Removes rows missing the core outcome, age, or participant gender.\n- Uses the recorded mutual-match outcome (`match`) for match-rate comparisons.\n- Provides interactive filters for age, participant gender, and study wave.")
    st.markdown("#### Limitations")
    st.markdown("- The sample is historical and drawn from students at one university; it does not represent everyone.\n- A date-level row is directional, so two rows may describe the two people’s perspectives on the same date.\n- The charts describe associations and cannot establish cause and effect.\n- Categories and measures reflect the original study questionnaire and its time period.")
    st.markdown("#### Dataset and references")
    st.markdown("- Source file: [Speed Dating dataset (CSV)](https://datahub.io/core/openml-datasets/r/SpeedDating.csv)\n- Dataset description and original source reference: [Columbia University Big Data Analytics dataset list](https://www.ee.columbia.edu/~cylin/course/bigdata/getdatasetinfo.html)\n- Research background: [Fisman & Iyengar, Gender Differences in Mate Selection](https://www.nber.org/papers/w11276)")
    st.caption(f"Loaded locally from {DATA_PATH.name}; {len(data):,} usable rows after the app’s core-field cleaning step.")

st.divider()
st.markdown('<div class="source">The Match Lab · Built with Streamlit, pandas, and Plotly · Data used for educational exploration.</div>', unsafe_allow_html=True)
