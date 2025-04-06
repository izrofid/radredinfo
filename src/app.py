import streamlit as st

st.set_page_config(
    page_title="RR Locations",
    page_icon="https://raw.githubusercontent.com/JwowSquared/Radical-Red-Pokedex/master/favicon.ico",  # noqa: E501
)

pg = st.navigation(
    [
        st.Page("pokemon.py", title="Encounters"),
        st.Page("tms_and_hms.py", title="TMs/Hms & Tutors"),
    ]
)
pg.run()
