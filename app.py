###########################
#      Build web UI
###########################

import streamlit as st
from search import search, recommend

# Page title
st.title("🔍 Amazon Electronics Search + Recommender")

# Input box
query = st.text_input("Search for something:")

if query:
    results = search(query)

    st.subheader("Results")
    for _, row in results.iterrows():
        st.write(f"[**{row['title']}**]({row['url']})")
        st.write(row["description"])
        st.write(f"Score: {row['score']:.4f}")

        # Button for recommendations
        if st.button(f"Recommend similar for {row['id']}"):
            recs = recommend(row["id"])
            st.write("👉 Similar items:")
            for _, r in recs.iterrows():
                st.write(f"- [{r['title']}]({row['url']})")