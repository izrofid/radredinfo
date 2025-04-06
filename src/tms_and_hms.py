import streamlit as st
import pandas as pd

# Load TM/HM data
tm_df = pd.read_csv("data/tms.csv")
hm_df = pd.read_csv("data/hms.csv")
tutor_df = pd.read_csv("data/tutors.csv")


def render_custom_table(df):
    rows_html = ""
    for _, row in df.iterrows():

        if "Tutor" in view:
            rows_html += f"""
            <tr>
                <td>{row['Move']}</td>
                <td>{row['Location']}</td>
                <td>{row['Cost']}</td>
            </tr>
        """
            firstrow = "Move"
            secondrow = "Location"
            thirdrow = "Cost"
        else:
            rows_html += f"""
            <tr>
                <td>{row['Number']}</td>
                <td>{row['Move']}</td>
                <td>{row['Location']}</td>
            </tr>
            """
            firstrow = "TM/HM"
            secondrow = "Move"
            thirdrow = "Location"

    table_html = f"""
    <style>
    .custom-table {{
        border-collapse: collapse;
        width: 100%;
        font-family: 'Segoe UI', sans-serif;
    }}
    .custom-table th, .custom-table td {{
        border-bottom: 1px solid #444;
        text-align: left;
        padding: 12px 16px;
    }}
    .custom-table tr:hover {{
        background-color: #333;
    }}
    .custom-table th {{
        background-color: #222;
        color: #eee;
    }}
    </style>

    <table class="custom-table">
        <thead>
            <tr>
                <th>{firstrow}</th>
                <th>{secondrow}</th>
                <th>{thirdrow}</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """

    st.html(table_html)


st.title("Radical Red TM/HM Locations")
st.markdown(
    "Search for a TM or HM to find where and at what levels it can be encountered."  # noqa: E501
)

col1, col2 = st.columns(2)
with col2:
    view = st.radio(
        "View TMs, Hms or Tutors?", ["📀 TMs", "💿 HMs", "📕Tutors"], horizontal=True
    )

if "TMs" in view:
    df = tm_df
elif "HMs" in view:
    df = hm_df
else:
    df = tutor_df

if "Move" in df.columns:
    move_options = sorted(df["Move"].unique())
else:
    move_options = []

with col1:
    selected_move = st.selectbox("Select a move:", options=["All"] + move_options)
    if selected_move != "All":
        df = df[df["Move"] == selected_move]


render_custom_table(df)
