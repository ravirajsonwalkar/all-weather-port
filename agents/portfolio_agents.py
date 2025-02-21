from langchain_community.llms import OpenAI
import yfinance as yf
from typing import Dict
from transformers import pipeline

class MarketAnalysisAgent:
    def __init__(self):
        self.llm = pipeline("text-generation", model="mistralai/Mistral-7B-v0.1")

    def analyze_market(self):
        prompt = "Analyze the current stock market trend based on historical performance."
        response = self.llm(prompt, max_length=100, do_sample=True)
        return response[0]['generated_text']

        
    def analyze_market(self) -> Dict:
        """Analyze current market conditions"""
        try:
            spy = yf.Ticker("SPY")
            data = spy.history(period="1mo")
            return {
                "volatility": data['Close'].std(),
                "trend": "bullish" if data['Close'][-1] > data['Close'][0] else "bearish"
            }
        except Exception as e:
            return {"error": f"Could not fetch market data: {str(e)}"}

class PortfolioAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0.2)
        
    def get_allocation(self, age: int, risk: str) -> Dict:
        """Get portfolio allocation based on age and risk tolerance"""
        allocations = {
            "Low": {"stocks": 40, "bonds": 50, "cash": 10},
            "Moderate": {"stocks": 60, "bonds": 30, "cash": 10},
            "High": {"stocks": 80, "bonds": 15, "cash": 5}
        }
        
        if risk not in allocations:
            return {"error": "Invalid risk level. Choose from Low, Moderate, or High."}
        
        age_factor = (100 - age) / 100
        base = allocations[risk]
        
        return {
            "stocks": base["stocks"] * age_factor,
            "bonds": base["bonds"] + (base["stocks"] * (1 - age_factor)) * 0.7,
            "cash": base["cash"] + (base["stocks"] * (1 - age_factor)) * 0.3
        }

class ImplementationAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
    
    def create_plan(self, allocation: Dict, monthly_invest: float) -> Dict:
        """Generate an implementation plan for investing"""
        return {
            "monthly_investments": {
                "stocks": monthly_invest * (allocation["stocks"] / 100),
                "bonds": monthly_invest * (allocation["bonds"] / 100),
                "cash": monthly_invest * (allocation["cash"] / 100)
            },
            "recommended_etfs": {
                "stocks": ["VTI", "VXUS"],
                "bonds": ["BND", "BNDX"],
                "cash": ["VMFXX"]
            },
            "rebalancing": "Quarterly"
        }

class AllWeatherPortfolioManager:
    def __init__(self):
        self.market_agent = MarketAnalysisAgent()
        self.portfolio_agent = PortfolioAgent()
        self.implementation_agent = ImplementationAgent()
    
    def generate_portfolio(self, age: int, risk_tolerance: str, monthly_investment: float) -> Dict:
        """Generate a personalized portfolio strategy"""
        # Fetch all required data
        result = {
            "market_analysis": self.market_agent.analyze_market(),
            "allocation": self.portfolio_agent.get_allocation(age, risk_tolerance),
            "summary": {
                "age": age,
                "risk_profile": risk_tolerance,
                "monthly_investment": monthly_investment
            }
        }
        
        # Generate investment plan
        result["implementation"] = self.implementation_agent.create_plan(
            result["allocation"], 
            monthly_investment
        )
        
        # Format the final output
        result["formatted_output"] = self.format_allocation(result)
        
        return result

    def format_allocation(self, result: Dict) -> str:
        """Format the portfolio report for better readability"""
        allocation = result["allocation"]
        monthly_invest = result["summary"]["monthly_investment"]
        market_analysis = result["market_analysis"]
        plan = result["implementation"]

        return f"""
        # 🎯 All-Weather Portfolio Report

        ## 📊 Market Analysis
        - **Volatility Level**: {"Low" if market_analysis['volatility'] < 15 else "Moderate" if market_analysis['volatility'] < 25 else "High"} ({market_analysis['volatility']:.2f}%)
        - **Market Trend**: 🚀 {market_analysis['trend'].title()}
        - **Market Outlook**: {"📈 Favorable for gradual entry" if market_analysis['trend'] == 'bullish' else "📉 Good time for dollar-cost averaging"}

        ---

        ## 💼 Portfolio Allocation
        - **Risk Profile**: {result["summary"]["risk_profile"]}
        - **Age**: {result["summary"]["age"]}
        - **Monthly Investment**: ${monthly_invest:.2f}

        ```mermaid
        pie title Asset Allocation
            "Stocks" : {allocation['stocks']:.1f}
            "Bonds" : {allocation['bonds']:.1f}
            "Cash" : {allocation['cash']:.1f}
        ```

        ### 🔍 Detailed Breakdown:
        | Asset Class  | Allocation (%) | Recommended ETFs | Monthly Investment |
        |-------------|--------------|------------------|--------------------|
        | **Stocks** 📈 | {allocation['stocks']:.1f}% | VTI (70%), VXUS (30%) | ${monthly_invest * allocation['stocks'] / 100:.2f} |
        | **Bonds** 🏛️ | {allocation['bonds']:.1f}% | BND (80%), BNDX (20%) | ${monthly_invest * allocation['bonds'] / 100:.2f} |
        | **Cash** 💵 | {allocation['cash']:.1f}% | VMFXX | ${monthly_invest * allocation['cash'] / 100:.2f} |

        ---

        ## 📈 Investment Growth Projection
        - Starting Monthly Investment: **${monthly_invest:.2f}**
        
        ```mermaid
        graph LR
            A[Start] --> B[10 Years]
            B --> C[20 Years]
            C --> D[30 Years]
        ```

        **Growth Estimates**:
        - 📊 **Conservative (6% Return)**:  
          - 10 Years: **${monthly_invest * 12 * 10 * 1.06**10:.2f}**
          - 20 Years: **${monthly_invest * 12 * 20 * 1.06**20:.2f}**
          - 30 Years: **${monthly_invest * 12 * 30 * 1.06**30:.2f}**
        
        - 🚀 **Expected (8% Return)**:  
          - 10 Years: **${monthly_invest * 12 * 10 * 1.08**10:.2f}**
          - 20 Years: **${monthly_invest * 12 * 20 * 1.08**20:.2f}**
          - 30 Years: **${monthly_invest * 12 * 30 * 1.08**30:.2f}**

        ---

        ## 📝 Implementation Plan
        ### ✅ Step 1: Account Setup
        - 🏦 Open brokerage account (**Vanguard, Fidelity, Schwab**)
        - 🔄 Set up **${monthly_invest:.2f}** automatic monthly investments  
        - 🔁 Enable **Dividend Reinvestment (DRIP)**  

        ### 🔄 Step 2: Rebalancing Strategy
        - ✅ Monitor for **5% asset drift**
        - 🔁 Adjust portfolio every **quarter**
        - 📊 Review market & personal financial changes

        ---

        ## 🛡 Risk Management
        - ✅ **Diversification** across multiple asset classes  
        - 🔄 **Regular Rebalancing** to maintain risk  
        - 📉 **Dollar-Cost Averaging** for market fluctuations  
        - 🏦 **Emergency Fund** maintained at **{allocation['cash']:.1f}%**  

        ---

        ## 📚 Recommended Reading
        - 📖 [Bridgewater All-Weather Portfolio](https://www.bridgewater.com/research-and-insights/the-all-weather-story)  
        - 📖 [Bogleheads Investment Philosophy](https://www.bogleheads.org/wiki/Bogleheads®_investment_philosophy)  
        - 📖 [Risk Parity Explained](https://www.investopedia.com/terms/r/risk-parity.asp)  

        🚀 **Take Action Now!** 🏦 Open your brokerage, set up investments, and grow your wealth!
        """

# ✅ Now, just instantiate and call:
# manager = AllWeatherPortfolioManager()
# report = manager.generate_portfolio(30, "Moderate", 1000)
# print(report["formatted_output"])
