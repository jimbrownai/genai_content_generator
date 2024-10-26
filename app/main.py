import  streamlit as st
from utils import clean_text
from portfolio import Portfolio
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain


def create_streamlit_app(llm,portfolio,clean_text):
    st.title("Generator")
    url_input = st.text_input("Enter the url",value="https:")
    submit_button = st.button("Submit")

    if submit_button:
        try:

            loader = WebBaseLoader([url_input])
            data= clean_text(loader.load().pop().page_content)

            jobs = llm.extract_data(data)
            portfolio.load_portfolio()

            for job in jobs:
                skills = job.get('skills',[])
                links = portfolio.query_links(skills)

                email = llm.write_email(job,links)
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__== "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout='wide',page_title='Content Generator')
    create_streamlit_app(chain,portfolio,clean_text)