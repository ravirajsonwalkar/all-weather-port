# Add at the start of app.py
import tracemalloc
import time

def track_performance(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage: {current / 10**6}MB")
        print(f"Peak memory usage: {peak / 10**6}MB")
        print(f"Time taken: {time.time() - start_time} seconds")
        
        tracemalloc.stop()
        return result
    return wrapper

import streamlit as st
import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf
from typing import Dict

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from transformers import pipeline
from utils.explanations import PORTFOLIO_INTRO, INPUT_EXPLANATIONS
import os
from huggingface_hub import login

st.cache_resource 
st.cache_data

@st.cache_resource
def load_transformers():
    from transformers import pipeline
    return pipeline

@st.cache_resource
def load_openai():
    from langchain_community.llms import OpenAI
    return OpenAI

hf_token = os.getenv("HUGGINGFACE_TOKEN")

if hf_token:
    login(hf_token)  # ✅ Correct way to call login
else:
    raise ValueError("Hugging Face Token not found! Make sure it's set in Secrets.")

# Initialize LLM using Gemma-2B with authentication
llm = pipeline("text-generation", model="google/gemma-2b", token=hf_token, device=-1)

def plot_pie_chart(allocation):
    labels = ["Stocks", "Bonds", "Cash"]
    sizes = [allocation['stocks'], allocation['bonds'], allocation['cash']]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig)

def plot_growth_projection(monthly_investment):
    years = [10, 20, 30]
    conservative_growth = [monthly_investment * 12 * y * 1.06**y for y in years]
    expected_growth = [monthly_investment * 12 * y * 1.08**y for y in years]
    
    df = pd.DataFrame({
        "Years": years,
        "Conservative Growth (6%)": conservative_growth,
        "Expected Growth (8%)": expected_growth
    })
    df_melted = df.melt("Years", var_name="Growth Type", value_name="Amount")
    
    chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x=alt.X("Years:O", title="Investment Duration (Years)"),
        y=alt.Y("Amount:Q", title="Projected Portfolio Value ($)"),
        color="Growth Type"
    ).properties(title="Investment Growth Projection")
    
    st.altair_chart(chart, use_container_width=True)

def analyze_market():
    prompt = "Analyze the current stock market trend based on historical performance."
    response = llm(prompt, max_length=100, do_sample=True)
    return response[0]['generated_text']

def main():
    # Add loading indicators and error handling
    st.set_page_config(
        page_title="All-Weather Portfolio Generator", 
        page_icon="💼",
        initial_sidebar_state="collapsed"
    )

    # Use st.spinner for long-running tasks
    with st.spinner('Initializing portfolio generator...'):
        try:
            # Lazy load heavy components
            portfolio_manager = st.cache_resource(AllWeatherPortfolioManager)()
        except Exception as e:
            st.error(f"Initialization Error: {e}")
            return
    
    print("✅ Streamlit app is running...")

    st.title("All-Weather Portfolio Generator")

    # Explanation Before Disclaimer
    st.markdown(PORTFOLIO_INTRO)

    # Disclaimer
    st.markdown("""
    ### ⚠️ Important Disclaimer
    This tool is for **educational purposes only** and **does not constitute financial advice**. 
    Please consult a **certified financial advisor** before making investment decisions.
    Results are based on general financial theories and **may not suit individual circumstances**.
    """)

    # ✅ Initialize session state if it doesn’t exist
    if "generated" not in st.session_state:
        st.session_state.generated = False

    # User Input Section
    st.header("Create Your Portfolio")

    with st.expander("Understanding the Inputs"):
        for param, explanation in INPUT_EXPLANATIONS.items():
            st.write(f"**{param.title()}**: {explanation}")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, value=26, key="age")
        monthly_investment = st.number_input("Monthly Investment ($)", min_value=100, value=1500, step=100, key="monthly_investment")

    with col2:
        risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Moderate", "High"], index=2, key="risk_tolerance")

    # ✅ Add a "Generate Portfolio" button
    if st.button("Generate Portfolio"):
        st.session_state.generated = True  # ✅ Set session state to True when button is clicked

    # ✅ Only run portfolio generation if the button has been clicked
    if st.session_state.generated:
        with st.spinner("Creating your personalized portfolio..."):
            portfolio_manager = AllWeatherPortfolioManager()
            try:
                result = portfolio_manager.generate_portfolio(
                    age=st.session_state.age,
                    risk_tolerance=st.session_state.risk_tolerance,
                    monthly_investment=st.session_state.monthly_investment
                )

                if not result or "summary" not in result:
                    st.error("❌ Failed to generate portfolio. Please try again.")
                    return
            except Exception as e:
                st.error(f"❌ Error generating portfolio: {e}")
                return

            st.success("Your All-Weather Portfolio Plan is Ready!")

            # Market Analysis
            st.subheader("Market Analysis")
            st.markdown(f"""
            - **Volatility Level**: {result["market_analysis"]["volatility"]:.2f}%
            - **Market Trend**: {result["market_analysis"]["trend"].title()}
            - **Market Outlook**: Favorable for gradual entry if bullish, consider Dollar Cost Averaging if bearish
            """)

            # Portfolio Allocation
            st.subheader("Portfolio Allocation")
            plot_pie_chart(result["allocation"])

            # Investment Growth Projection
            st.subheader("📈 Investment Growth Projection")
            plot_growth_projection(st.session_state.monthly_investment)

            # ✅ Fix missing monthly investment value
            st.subheader("📌 Implementation Plan")
            st.markdown(f"""
            1. **Open a brokerage account** (Vanguard, Fidelity, Schwab).
            2. **Set up automatic investments** of **${st.session_state.monthly_investment:.2f}** per month.
            3. **Enable Dividend Reinvestment (DRIP)** to maximize compounding returns. DRIP automatically reinvests dividends into more shares, enhancing long-term growth potential.
            4. **Monitor and rebalance** quarterly based on portfolio performance to maintain asset allocation.
            """)

            # Contact & Collaboration
            st.markdown("""
            ### 🤝 Contact & Collaboration
            If you're interested in collaborating, building on top of this project, or need more information, feel free to reach out:
            - 📧 Email: **raviwork2802@gmail.com** or **alphaport99@gmail.com**
            """)

            # Final Disclaimer
            st.markdown("""
            ### ⚠️ Final Reminder
            This tool is for **educational purposes only** and **does not constitute financial advice**.
            """)


