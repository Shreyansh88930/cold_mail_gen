import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# ---------------------- UI Setup ---------------------- #
st.set_page_config(
    page_title="Cold Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_streamlit_app(llm, portfolio, clean_text):
    # Header
    st.markdown(
        """
        <style>
            .main-title {
                font-size: 2.2rem;
                font-weight: bold;
                color: #2E86C1;
            }
            .sub-text {
                font-size: 1rem;
                color: #566573;
            }
            .stTextInput > div > div > input {
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #D6DBDF;
            }
            .stButton>button {
                background-color: #2E86C1;
                color: white;
                font-weight: 600;
                border-radius: 10px;
                padding: 0.6em 1.2em;
                border: none;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #1B4F72;
                transform: scale(1.02);
            }
            .email-box {
                background: #ffffff;  /* clean white background */
                padding: 1.2rem;
                border-radius: 12px;
                margin-top: 1rem;
                box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
                border: 1px solid #D6DBDF;
                white-space: pre-wrap;  /* Preserve line breaks */
                font-family: "Courier New", monospace;
                font-size: 1rem;
                color: #2C3E50;  /* dark text for readability */
                line-height: 1.5;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='main-title'>📧 Cold Email Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Generate personalized cold emails from job postings in seconds 🚀</div>", unsafe_allow_html=True)

    # Input
    with st.container():
        url_input = st.text_input("🔗 Enter Job Posting URL:", value="https://jobs.nike.com/job/R-33460")
        submit_button = st.button("✨ Generate Email")

    # Processing
    if submit_button:
        try:
            with st.spinner("⏳ Fetching job details and generating email..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)

                    st.markdown("#### ✉️ Generated Cold Email")
                    st.markdown(
                        f"<div class='email-box'>{email.replace(chr(10), '<br>')}</div>",
                        unsafe_allow_html=True
                    )

        except Exception as e:
            st.error(f"⚠️ An Error Occurred: {e}")


# ---------------------- App Runner ---------------------- #
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
