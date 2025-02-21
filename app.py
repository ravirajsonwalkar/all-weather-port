import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

def all_weather_portfolio_strategy(age, risk_tolerance, monthly_investment):
    """
    All-Weather Portfolio Strategy Based on Ray Dalio's Principles
    """
    # Base allocations inspired by All-Weather Portfolio concept
    base_allocation = {
        "Stocks": 30,           # Domestic & International Equities
        "Long-Term Bonds": 40,  # Government Bonds
        "Intermediate Bonds": 15,  # Corporate Bonds
        "Gold": 7.5,            # Inflation hedge
        "Commodities": 7.5      # Inflation protection
    }
    
    # Risk and age adjustment
    risk_multipliers = {
        "Low": 0.7,
        "Moderate": 1.0,
        "High": 1.3
    }
    
    # Age-based risk reduction
    age_risk_factor = max(0.5, (100 - age) / 100)
    
    # Adjust allocation based on risk tolerance and age
    adjusted_allocation = {
        asset: round(weight * risk_multipliers.get(risk_tolerance, 1.0) * age_risk_factor, 1)
        for asset, weight in base_allocation.items()
    }
    
    # Normalize to ensure 100%
    total = sum(adjusted_allocation.values())
    normalized_allocation = {
        asset: round((weight / total) * 100, 1)
        for asset, weight in adjusted_allocation.items()
    }
    
    # Projected growth calculations
    def calculate_growth(rate):
        return [
            round(monthly_investment * 12 * years * (1 + rate)**years, 2)
            for years in [10, 20, 30]
        ]
    
    return {
        "allocation": normalized_allocation,
        "investment_projections": {
            "conservative_6%": calculate_growth(0.06),
            "expected_8%": calculate_growth(0.08)
        },
        "key_principles": [
            "Balanced across economic conditions",
            "Reduced portfolio volatility",
            "Protection against inflation and market downturns"
        ]
    }

def main():
    st.title("🌐 All-Weather Portfolio Generator")
    
    # Sidebar for explanation
    st.sidebar.markdown("""
    ### 🌍 All-Weather Portfolio Concept
    Developed by Ray Dalio, this strategy aims to:
    - Perform well in any economic condition
    - Balance risk across different asset classes
    - Provide consistent returns
    """)
    
    # Input columns
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, value=35)
        monthly_investment = st.number_input("Monthly Investment ($)", min_value=100, value=1000)
    
    with col2:
        risk_tolerance = st.selectbox(
            "Risk Tolerance", 
            ["Low", "Moderate", "High"], 
            index=1
        )
    
    # Generate Portfolio Button
    if st.button("Generate All-Weather Portfolio"):
        with st.spinner("Crafting your resilient portfolio..."):
            result = all_weather_portfolio_strategy(age, risk_tolerance, monthly_investment)
            
            # Portfolio Allocation Visualization
            st.header("🏦 Portfolio Allocation")
            allocation_df = pd.DataFrame.from_dict(
                result['allocation'], 
                orient='index', 
                columns=['Percentage']
            ).reset_index()
            allocation_df.columns = ['Asset', 'Allocation']
            
            # Pie Chart
            fig, ax = plt.subplots()
            ax.pie(
                allocation_df['Allocation'], 
                labels=allocation_df['Asset'], 
                autopct='%1.1f%%'
            )
            ax.set_title("Asset Class Distribution")
            st.pyplot(fig)
            
            # Detailed Allocation Table
            st.table(allocation_df.set_index('Asset'))
            
            # Investment Projections
            st.header("📈 Long-Term Projection")
            projection_df = pd.DataFrame({
                'Duration': ['10 Years', '20 Years', '30 Years'],
                'Conservative (6%)': result['investment_projections']['conservative_6%'],
                'Expected (8%)': result['investment_projections']['expected_8%']
            })
            
            # Line Chart for Projections
            projection_chart = alt.Chart(projection_df.melt('Duration')).mark_line(point=True).encode(
                x='Duration:N',
                y='value:Q',
                color='variable:N',
                tooltip=['Duration', 'value']
            ).properties(title='Investment Growth Projection')
            
            st.altair_chart(projection_chart, use_container_width=True)
            
            # Key Principles
            st.header("🛡️ Portfolio Principles")
            for principle in result['key_principles']:
                st.write(f"- {principle}")
            
            # Disclaimer
            st.markdown("""
            ### ⚠️ Disclaimer
            This is an educational tool. Always consult a financial advisor 
            before making investment decisions.
            """)

if __name__ == "__main__":
    main()
