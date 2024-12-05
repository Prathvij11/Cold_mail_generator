#https://careers.ibm.com/job/21093624/al-solution-architect-bangalore-in/?codes=WEB_SEARCH_INDIA
#import streamlit,langchain,langchain-community,langchain-core,langchain-groq,beautifulsoup4,pandas,chromadb,dotenv

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader   
from llm import Llm
from portfolio import Portfolio


def create_streamlit_app(llm, portfolio):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://careers.ibm.com/job/21087745/storage-software-engineer-c-c-cloud-bangalore-in/?codes=WEB_SEARCH_INDIA")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])      #web scrapping
            data = loader.load().pop().page_content   #page content only(text)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            if not jobs:  # Check if jobs list is empty
                st.warning("No job descriptions found at the provided URL.")
            else:
                for job in jobs:                        #if there is multiple jobs
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    llm = Llm()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(llm, portfolio)

