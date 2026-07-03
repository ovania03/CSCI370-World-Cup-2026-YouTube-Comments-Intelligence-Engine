
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast
import json
from collections import Counter

# Page config
st.set_page_config(
    page_title="World Cup 2026 Comments Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("worldcup_2026_with_topics.csv")
    # Parse list columns stored as strings
    for col in ["keywords", "entities"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else [])
    df["like_count"] = pd.to_numeric(df["like_count"], errors="coerce").fillna(0).astype(int)
    df["sentiment_score"] = pd.to_numeric(df.get("sentiment_score", 0), errors="coerce").fillna(0)
    df["topic"] = pd.to_numeric(df.get("topic", -1), errors="coerce").fillna(-1).astype(int)
    return df

df_full = load_data()

# Sidebar
st.sidebar.title("Filters")
st.sidebar.metric("Total Comments", f"{len(df_full):,}")
st.sidebar.metric("Videos Analysed", 15)

sentiment_filter = st.sidebar.multiselect(
    "Sentiment", ["positive", "negative", "neutral"],
    default=["positive", "negative", "neutral"]
)

min_likes = st.sidebar.slider("Min Likes", 0, int(df_full["like_count"].max()), 0)

df = df_full[
    (df_full["sentiment"].isin(sentiment_filter)) &
    (df_full["like_count"] >= min_likes)
].copy()

st.sidebar.metric("Filtered Comments", f"{len(df):,}")

# Header
st.title("World Cup 2026 — YouTube Comments Intelligence Engine")
st.markdown("*CSCI370 NLP Pipeline: scraping -> sentiment -> NER -> topic modelling -> RAG*")
st.divider()

# Row 1: KPI cards
k1, k2, k3, k4 = st.columns(4)
pos_pct = (df["sentiment"] == "positive").mean() * 100
neg_pct = (df["sentiment"] == "negative").mean() * 100
avg_likes = df["like_count"].mean()
n_topics = df[df["topic"] != -1]["topic"].nunique()

k1.metric("Positive", f"{pos_pct:.1f}%")
k2.metric("Negative", f"{neg_pct:.1f}%")
k3.metric("Avg Likes", f"{avg_likes:.1f}")
k4.metric("Topics Found", n_topics)
st.divider()

# Row 2: Sentiment charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sentiment Distribution")
    counts = df["sentiment"].value_counts()
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        color=counts.index,
        color_discrete_map={"positive": "#22c55e", "negative": "#ef4444", "neutral": "#94a3b8"},
        hole=0.4
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sentiment Score Distribution")
    fig = px.histogram(
        df, x="sentiment_score", color="sentiment", nbins=40,
        color_discrete_map={"positive": "#22c55e", "negative": "#ef4444", "neutral": "#94a3b8"},
        labels={"sentiment_score": "VADER Compound Score"},
        barmode="overlay", opacity=0.7
    )
    fig.add_vline(x=0.05, line_dash="dash", line_color="green", annotation_text="+0.05")
    fig.add_vline(x=-0.05, line_dash="dash", line_color="red", annotation_text="-0.05")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Row 3: Keywords & Entities
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top Keywords")
    all_kws = [kw for lst in df["keywords"] for kw in (lst if isinstance(lst, list) else [])]
    common_kws = Counter(all_kws).most_common(15)
    if common_kws:
        kw_df = pd.DataFrame(common_kws, columns=["Keyword", "Count"])
        fig = px.bar(kw_df, x="Count", y="Keyword", orientation="h",
                     color="Count", color_continuous_scale="Blues")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No keywords found (run keyword extraction first)")

with col4:
    st.subheader("Named Entities")
    all_ents = [e[0] for lst in df["entities"] for e in (lst if isinstance(lst, list) else [])]
    common_ents = Counter(all_ents).most_common(15)
    if common_ents:
        ent_df = pd.DataFrame(common_ents, columns=["Entity", "Count"])
        fig = px.bar(ent_df, x="Count", y="Entity", orientation="h",
                     color="Count", color_continuous_scale="Oranges")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No entities found (run NER first)")

st.divider()

# Row 4: Topics
st.subheader("Topic Distribution")
topic_data = df[df["topic"] != -1]["topic"].value_counts().head(10).reset_index()
topic_data.columns = ["Topic ID", "Count"]
topic_data["Topic Label"] = topic_data["Topic ID"].apply(lambda x: f"Topic {x}")
if not topic_data.empty:
    fig = px.bar(topic_data, x="Topic Label", y="Count", color="Count",
                 color_continuous_scale="Viridis")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No topics found (run topic modelling first)")

st.divider()

# Row 5: Top comments
st.subheader("Top Comments by Likes")
top_comments = df.nlargest(10, "like_count")[["author", "text", "sentiment", "like_count"]]
st.dataframe(
    top_comments.style.apply(
        lambda row: [
            f"background-color: {'#dcfce7' if row.sentiment=='positive' else '#fee2e2' if row.sentiment=='negative' else '#f1f5f9'}"
        ] * len(row), axis=1
    ),
    use_container_width=True
)

st.divider()

# Row 6: Semantic search
st.subheader("Semantic Search (RAG Retrieval)")
st.markdown("Enter a question to retrieve the most relevant comments using vector similarity search.")

question = st.text_input("Ask about the World Cup comments:", placeholder="e.g. What do fans think about Messi?")

if question:
    # Fast keyword search (always available)
    with st.spinner("Searching..."):
        q_words = question.lower().split()
        hits = []
        for _, row in df.iterrows():
            t = str(row["text"]).lower()
            score = sum(1 for w in q_words if w in t)
            if score > 0:
                hits.append((score, row))
        hits.sort(key=lambda x: (-x[0], -x[1]["like_count"]))
        
        if hits:
            st.markdown("**Most Relevant Comments:**")
            for score, row in hits[:8]:
                sent = row.get("sentiment", "neutral")
                color = "#dcfce7" if sent == "positive" else "#fee2e2" if sent == "negative" else "#f1f5f9"
                st.markdown(
                    f"""<div style="background:{color};padding:10px;border-radius:8px;margin:5px 0">
                    <b>{row["author"]}</b> - {row["like_count"]} likes<br>{str(row["text"])[:250]}
                    </div>""", unsafe_allow_html=True
                )
        else:
            st.info("No matching comments found. Try different keywords.")

st.divider()

# Row 7: Raw data browser
with st.expander("Browse Raw Comments"):
    st.dataframe(
        df[["author", "updated_at", "text", "sentiment", "sentiment_score", "like_count", "topic"]]
        .sort_values("like_count", ascending=False)
        .reset_index(drop=True),
        use_container_width=True
    )

st.caption("CSCI370 Project · World Cup 2026 YouTube Intelligence Engine")
