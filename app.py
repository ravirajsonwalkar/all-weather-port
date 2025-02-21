import streamlit as st
import os
import sys

# Add performance monitoring
import tracemalloc
import time

# Optimize imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf

# Caching decorators
st.set_page_config(page_title="All-Weather Portfolio Generator", page_icon="💼")

# Lazy loading of heavy libraries
@st.cache_resource
def load_transformers():
    from transformers import pipeline
    return pipeline

@st.cache_resource
def load_openai():
    from langchain_community.llms import OpenAI
    return OpenAI

# Performance tracking decorator
def track_performance(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        current, peak = tracemalloc.get_traced_memory()
        st.write(f"Memory usage: Current {current/10**6}MB, Peak {peak/10**6}MB")
        st.write(f"Time taken: {time.time() - start_time} seconds")
        
        tracemalloc.stop()
        return result
    return wrapper

# Safe portfolio generation
def safe_portfolio_generation(age, risk, monthly_invest):
    try:
        # Use cached resource
        manager = st.cache_resource(AllWeatherPortfolioManager)()
        return manager.generate_portfolio(age, risk, monthly_invest)
    except Exception as e:
        st.error(f"Portfolio generation failed: {e}")
        # Provide a default conservative portfolio
        return {
            "allocation": {"stocks": 50, "bonds": 40, "cash": 10},
            "market_analysis": {"volatility": 15, "trend": "neutral"}
        }

def main():
    st.title("All-Weather Portfolio Generator")

    # Use expanders to reduce initial page load
    with st.expander("What is an All-Weather Portfolio?"):
        st.markdown(PORTFOLIO_INTRO)

    # Input Section with Caching
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, value=26, key="age")
        monthly_investment = st.number_input("Monthly Investment ($)", min_value=100, value=1500, step=100, key="monthly_investment")

    with col2:
        risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Moderate", "High"], index=2, key="risk_tolerance")

    # Generate Portfolio Button with Session State
    if st.button("Generate Portfolio"):
        with st.spinner("Creating your personalized portfolio..."):
            result = safe_portfolio_generation(age, risk_tolerance, monthly_investment)
            
            # Display results
            if result:
                st.success("Your All-Weather Portfolio Plan is Ready!")
                
                # Market Analysis Section
                st.subheader("Market Analysis")
                st.markdown(f"""
                - **Volatility Level**: {result["market_analysis"].get("volatility", "N/A"):.2f}%
                - **Market Trend**: {result["market_analysis"].get("trend", "Neutral").title()}
                """)

                # Portfolio Allocation Visualization
                plot_pie_chart(result.get("allocation", {}))
                plot_growth_projection(monthly_investment)

# Performance Monitoring
@track_performance
def run_app():
    main()

if __name__ == "__main__":
    run_app()
