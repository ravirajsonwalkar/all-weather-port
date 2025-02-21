import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import yfinance as yf

def plot_pie_chart(allocation):
    labels = ["Stocks", "Bonds", "Cash"]
    sizes = [allocation.get('stocks', 60), 
             allocation.get('bonds', 30), 
             allocation.get('cash', 10)]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis("equal")
    
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
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Years:O", title="Investment Duration (Years)"),
        y=alt.Y("value:Q", title="Projected Portfolio Value ($)"),
        color="variable:N"
    ).properties(title="Investment Growth Projection")
    
    st.altair_chart(chart, use_container_width=True)

def generate_portfolio(age, risk, monthly_investment):
    # Simple portfolio allocation logic
    allocations = {
        "Low": {"stocks": 40, "bonds": 50, "cash": 10},
        "Moderate": {"stocks": 60, "bonds": 30, "cash": 10},
        "High": {"stocks": 80, "bonds": 15, "cash": 5}
    }
    
    # Adjust allocation based on age
    allocation = allocations.get(risk, allocations["Moderate"])
    age_factor = max(0.5, (100 - age) / 100)
    
    return {
        "allocation": {
            "stocks": allocation["stocks"] * age_factor,
            "bonds": allocation["bonds"] + (allocation["stocks"] * (1 - age_factor)) * 0.7,
            "cash": allocation["cash"] + (allocation["stocks"] * (1 - age_factor)) * 0.3
        },
        "market_analysis": {
            "volatility": 15,
            "trend": "Neutral"
        }
    }

def main():
    st.title("Simple Portfolio Generator")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, value=30)
        monthly_investment = st.number_input("Monthly Investment ($)", min_value=100, value=1000)
    
    with col2:
        risk_tolerance = st.selectbox("Risk Tolerance", ["Low", "Moderate", "High"])
    
    # Generate Portfolio Button
    if st.button("Generate Portfolio"):
        with st.spinner("Creating your portfolio..."):
            result = generate_portfolio(age, risk_tolerance, monthly_investment)
            
            st.success("Portfolio Generated!")
            
            # Market Analysis
            st.subheader("Market Analysis")
            st.write(f"Volatility: {result['market_analysis']['volatility']}%")
            st.write(f"Market Trend: {result['market_analysis']['trend']}")
            
            # Portfolio Allocation
            st.subheader("Portfolio Allocation")
            plot_pie_chart(result['allocation'])
            
            # Growth Projection
            st.subheader("Investment Growth Projection")
            plot_growth_projection(monthly_investment)
            
            # Additional Details
            st.subheader("Portfolio Details")
            st.write(f"Stocks: {result['allocation']['stocks']:.1f}%")
            st.write(f"Bonds: {result['allocation']['bonds']:.1f}%")
            st.write(f"Cash: {result['allocation']['cash']:.1f}%")

if __name__ == "__main__":
    main()
