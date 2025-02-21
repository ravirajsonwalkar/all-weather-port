import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

def all_weather_portfolio_strategy(age, risk_tolerance, monthly_investment):
    """
    Comprehensive All-Weather Portfolio Strategy
    """
    # Detailed asset allocation based on Ray Dalio's principles
    base_allocation = {
        "US Stocks": 15,            # Domestic large-cap equities
        "International Stocks": 10, # Global market exposure
        "Long-Term US Treasuries": 40,  # Protection during economic downturns
        "Intermediate-Term Treasuries": 15,  # Balanced fixed income
        "Treasury Inflation-Protected Securities (TIPS)": 7.5,  # Inflation protection
        "Gold": 7.5,                # Ultimate hedge against uncertainty
        "Commodities": 5            # Inflation and economic cycle hedge
    }
    
    # Risk and age adjustment factors
    risk_multipliers = {
        "Low": 0.8,
        "Moderate": 1.0,
        "High": 1.2
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
        "economic_scenarios": [
            {
                "name": "Rising Growth & Rising Inflation",
                "description": "Economy expanding, prices increasing",
                "best_performers": ["Commodities", "Stocks", "TIPS"]
            },
            {
                "name": "Rising Growth & Falling Inflation",
                "description": "Economic expansion with stable prices",
                "best_performers": ["Stocks", "Intermediate Bonds"]
            },
            {
                "name": "Falling Growth & Rising Inflation",
                "description": "Economic slowdown with increasing prices",
                "best_performers": ["Gold", "TIPS", "Commodities"]
            },
            {
                "name": "Falling Growth & Falling Inflation",
                "description": "Economic contraction with decreasing prices",
                "best_performers": ["Long-Term Treasuries"]
            }
        ]
    }

def add_resources_section():
    st.header("📚 All-Weather Portfolio Resources")
    
    # Books
    st.subheader("📖 Essential Books")
    books = [
        {
            "title": "Principles: Life and Work",
            "author": "Ray Dalio",
            "description": "The foundational book by Ray Dalio explaining his investment philosophy and the principles behind the All-Weather Portfolio",
            "link": "https://www.principles.com/"
        },
        {
            "title": "The Intelligent Investor",
            "author": "Benjamin Graham",
            "description": "A classic on value investing and portfolio strategy that influenced many modern investment approaches",
            "link": "https://www.amazon.com/Intelligent-Investor-Definitive-Value-Investing/dp/0060555661"
        },
        {
            "title": "A Random Walk Down Wall Street",
            "author": "Burton Malkiel",
            "description": "Provides insights into diversification and long-term investment strategies",
            "link": "https://www.amazon.com/Random-Walk-Down-Wall-Street/dp/0393352242"
        }
    ]
    
    book_cols = st.columns(3)
    for i, book in enumerate(books):
        with book_cols[i]:
            st.markdown(f"""
            **{book['title']}**
            *by {book['author']}*
            
            {book['description']}
            
            [Learn More]({book['link']})
            """)
    
    # Online Resources
    st.subheader("🌐 Online Learning Resources")
    resources = [
        {
            "title": "Bridgewater Associates All-Weather Strategy",
            "url": "https://www.bridgewater.com/research-and-insights/the-all-weather-story",
            "description": "Original research and insights from the creators of the All-Weather Portfolio"
        },
        {
            "title": "Investopedia - Risk Parity",
            "url": "https://www.investopedia.com/terms/r/risk-parity.asp",
            "description": "Detailed explanation of Risk Parity investment strategy"
        },
        {
            "title": "Bogleheads Investment Philosophy",
            "url": "https://www.bogleheads.org/wiki/Bogleheads®_investment_philosophy",
            "description": "Comprehensive guide to passive investing and portfolio construction"
        }
    ]
    
    for resource in resources:
        st.markdown(f"""
        ### {resource['title']}
        {resource['description']}
        
        [Explore Resource]({resource['url']})
        """)
    
    # Podcasts and Interviews
    st.subheader("🎧 Recommended Podcasts and Interviews")
    podcasts = [
        {
            "title": "Ray Dalio on TED Talk",
            "description": "Insights into economic principles and investment strategies",
            "link": "https://www.ted.com/talks/ray_dalio_how_to_build_a_company_where_the_best_ideas_win"
        },
        {
            "title": "Masters in Business with Barry Ritholtz",
            "description": "In-depth interviews with investment thought leaders",
            "link": "https://www.bloomberg.com/podcasts/masters_in_business"
        }
    ]
    
    for podcast in podcasts:
        st.markdown(f"""
        ### {podcast['title']}
        {podcast['description']}
        
        [Listen Now]({podcast['link']})
        """)
    
    # Financial Education Platforms
    st.subheader("🎓 Financial Education Platforms")
    platforms = [
        {
            "name": "Coursera - Investment and Portfolio Management",
            "description": "Online courses from top universities on investment strategies",
            "link": "https://www.coursera.org/courses?query=investment%20portfolio%20management"
        },
        {
            "name": "edX - Finance Courses",
            "description": "Academic-level courses on financial planning and investment",
            "link": "https://www.edx.org/learn/finance"
        }
    ]
    
    for platform in platforms:
        st.markdown(f"""
        ### {platform['name']}
        {platform['description']}
        
        [Explore Courses]({platform['link']})
        """)

def main():
    st.set_page_config(page_title="All-Weather Portfolio Generator", page_icon="💼", layout="wide")
    
    st.title("🌐 Comprehensive All-Weather Portfolio Generator")
    
    # Detailed Sidebar Explanation
    st.sidebar.markdown("""
    ## 🌍 The All-Weather Portfolio: A Deep Dive

    ### 🏛️ Origin
    Developed by Ray Dalio of Bridgewater Associates, the All-Weather Portfolio is a revolutionary investment strategy designed to perform consistently across different economic conditions.

    ### 🌈 Core Philosophy
    - **Diversification Beyond Traditional Approaches**
    - **Balanced Exposure to Different Economic Environments**
    - **Risk Parity: Balancing Risk, Not Just Allocation**

    ### 🛡️ Key Principles
    1. No single economic scenario should devastate the portfolio
    2. Spread investments across assets that react differently to economic changes
    3. Protect against both inflation and deflation
    4. Maintain steady growth regardless of market conditions
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
            
            # Create tabs
            tab1, tab2 = st.tabs(["Portfolio Details", "Learning Resources"])
            
            with tab1:
                # Portfolio Allocation Section
                st.header("🏦 Detailed Portfolio Allocation")
                allocation_df = pd.DataFrame.from_dict(
                    result['allocation'], 
                    orient='index', 
                    columns=['Allocation']
                ).reset_index()
                allocation_df.columns = ['Asset', 'Allocation']
                
                # Pie Chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.pie(
                    allocation_df['Allocation'], 
                    labels=allocation_df['Asset'], 
                    autopct='%1.1f%%'
                )
                ax.set_title("Asset Class Distribution", fontsize=16)
                st.pyplot(fig)
                
                # Detailed Allocation Table with Explanations
                # Replace the existing detailed allocation section with this code:

                # Detailed Allocation Table with Explanations
                st.subheader("🔍 Asset Class Breakdown")
                asset_details = {
                    "US Stocks": "Domestic large-cap equities providing growth potential",
                    "International Stocks": "Global market exposure for broader economic participation",
                    "Long-Term US Treasuries": "Safe-haven assets that perform well during economic downturns",
                    "Intermediate-Term Treasuries": "Balanced fixed income with moderate interest rate sensitivity",
                    "Treasury Inflation-Protected Securities (TIPS)": "Protects against inflation by adjusting principal with CPI",
                    "Gold": "Ultimate hedge against economic uncertainty and currency devaluation",
                    "Commodities": "Natural hedge against inflation and economic cycle variations"
                }
                
                detailed_allocation = allocation_df.copy()
                detailed_allocation['Description'] = detailed_allocation['Asset'].map(asset_details)
                
                # Calculate monthly investment for each asset class
                detailed_allocation['Monthly Investment'] = detailed_allocation['Allocation'].apply(
                    lambda x: f"${monthly_investment * (x/100):.2f}"
                )
                
                # Reorder columns for better readability
                detailed_allocation = detailed_allocation[['Asset', 'Allocation', 'Monthly Investment', 'Description']]
                
                # Display the dataframe
                st.dataframe(detailed_allocation)
                
                # Economic Scenarios Section
                st.header("🌍 Economic Scenario Analysis")
                for scenario in result['economic_scenarios']:
                    st.markdown(f"""
                    ### {scenario['name']}
                    **Description**: {scenario['description']}
                    **Best Performing Assets**: {', '.join(scenario['best_performers'])}
                    """)
                
                # Investment Projections
                st.header("📈 Long-Term Investment Projection")
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
                
                # Key Takeaways
                st.header("💡 Key Investment Insights")
                st.markdown("""
                1. **Diversification is Key**: No single asset dominates the portfolio
                2. **Balanced Risk Exposure**: Performs in multiple economic scenarios
                3. **Long-Term Perspective**: Focuses on consistent growth over time
                4. **Adaptive Strategy**: Adjusts with age and risk tolerance
                """)
                
                # Disclaimer
                st.markdown("""
                ### ⚠️ Important Disclaimer
                - This is an educational tool for illustrative purposes
                - Always consult a certified financial advisor
                - Past performance does not guarantee future results
                - Individual financial situations vary
                """)
            
            with tab2:
                # Resources Section
                add_resources_section()

if __name__ == "__main__":
    main()
