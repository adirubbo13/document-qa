import streamlit as st

# Automatically redirect to lab2.py
lab1_page = st.Page("pages/lab1.py", title = "Lab 1 Page")
lab2_page = st.Page("pages/lab2.py", title = "Lab 2 Page")


pg = st.navigation([lab2_page,lab1_page])
pg.run()
