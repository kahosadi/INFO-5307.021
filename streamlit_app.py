import streamlit as st

st.set_page_config(
    page_title = "Metadata Evaluator v0.1"
)

#st.title("Metadata Evaluator v0.1")

#sidebar
#with st.sidebar:
#    st.header("Menu")
#    st.subheader("Menu")
   
#page setup
main_page = st.Page(
    page = "views/main.py",
    title = "Main",
    default = True
)

authority_page = st.Page(
    page = "views/authority.py",
    title = "Name Headings"
)    

about_page = st.Page(
    page = "views/about.py",
    title = "About"
)    

pg = st.navigation(pages=[main_page, authority_page, about_page])

pg.run()
