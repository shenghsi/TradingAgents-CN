"""
Narrative Trend Analyst - US Stock Market
Analyzes short-term market narrative/focus and long-term trends
Provides ticker recommendations based on market analysis
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


def create_narrative_trend_analyst(llm, toolkit):
    """Create narrative trend analyst for US stock market"""
    
    def narrative_trend_analyst_node(state):
        print(f"📊 [DEBUG] ===== Narrative Trend Analyst Node Started =====")
        
        current_date = state["trade_date"]
        
        print(f"📊 [DEBUG] Input parameters: date={current_date}")
        print(f"📊 [DEBUG] Current state messages count: {len(state.get('messages', []))}")
        print(f"📊 [DEBUG] Existing narrative report: {state.get('narrative_trend_report', 'None')[:100]}...")
        
        print(f"📊 [Narrative Trend Analyst] Analyzing overall US market narrative and trends")
        print(f"📊 [DEBUG] Tool configuration check: online_tools={toolkit.config['online_tools']}")
        
        # Select tools based on configuration
        if toolkit.config["online_tools"]:
            # Use online tools for real-time data
            tools = [
                toolkit.get_realtime_stock_news,
                toolkit.get_global_news_openai,
                toolkit.get_google_news
            ]
            print(f"📊 [Narrative Trend Analyst] Using online tools for real-time analysis")
        else:
            # Use cached/offline tools
            tools = [
                toolkit.get_finnhub_news,
                toolkit.get_reddit_news,
                toolkit.get_google_news
            ]
            print(f"📊 [Narrative Trend Analyst] Using offline/cached tools")
        
        # Tool names for debugging
        tool_names_debug = []
        for tool in tools:
            if hasattr(tool, 'name'):
                tool_names_debug.append(tool.name)
            elif hasattr(tool, '__name__'):
                tool_names_debug.append(tool.__name__)
            else:
                tool_names_debug.append(str(tool))
        print(f"📊 [DEBUG] Selected tools: {tool_names_debug}")
        
        # Create system prompt for narrative trend analysis
        system_message = """You are a professional US stock market narrative and trend analyst. Your role is to analyze the overall market without focusing on specific stocks initially, and then provide specific ticker recommendations based on your analysis.

Your analysis should cover:

1. SHORT-TERM MARKET NARRATIVE/FOCUS (1-4 weeks):
   - Current market sentiment and dominant themes
   - Breaking news and events driving immediate market movements
   - Sector rotations and hot topics
   - Institutional flow patterns and retail sentiment
   - Key catalysts and upcoming events

2. LONG-TERM MARKET TRENDS (3-12 months):
   - Macroeconomic cycles and their current phase
   - Structural market changes and secular trends
   - Federal Reserve policy impacts and monetary cycle
   - Earnings cycle positioning and valuation trends
   - Technological disruption and innovation cycles

3. MARKET POSITION ASSESSMENT:
   - Where are we in the major trend cycles?
   - What are the key risks and opportunities?
   - Which sectors are leading/lagging?
   - What's driving institutional and retail flows?

4. TICKER RECOMMENDATIONS:
   - TOP 5-10 STOCKS TO BUY based on current narrative and trends
   - TOP 5-10 STOCKS TO AVOID/SELL based on current narrative and trends
   - Specific rationale for each recommendation
   - Risk assessment for each recommendation

Data sources to leverage:
- Recent financial news and market reports
- Sector performance and rotation analysis
- Economic indicators and Fed communications
- Institutional investment flows and insider activity
- Social media sentiment and retail trading patterns
- Earnings calendar and upcoming catalysts

Output Format:
1. Executive Summary of Current Market State
2. Short-term Market Narrative (1-4 weeks)
3. Long-term Trend Analysis (3-12 months)
4. Market Cycle Position Assessment
5. **BUY RECOMMENDATIONS** (5-10 tickers with rationale)
6. **SELL/AVOID RECOMMENDATIONS** (5-10 tickers with rationale)
7. Risk Factors and Key Monitoring Points

Focus on actionable insights and specific ticker recommendations for US stock market investors."""

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
            ("human", f"""Analyze the current US stock market narrative and trends as of {current_date}.

Please provide a comprehensive analysis that includes:

1. What is the current short-term market narrative driving movements?
2. Where are we in the long-term trend cycles?
3. What are the key opportunities and risks in the current environment?
4. Based on this analysis, what are the TOP stocks to BUY right now?
5. What are the TOP stocks to AVOID or SELL right now?

For each stock recommendation, provide:
- Ticker symbol
- Company name
- Specific rationale based on current market narrative
- Risk assessment
- Potential upside/downside

Use the available tools to gather the latest market data, news, and sentiment indicators to support your analysis.""")
        ])
        
        # Create agent
        from langchain.agents import create_react_agent, AgentExecutor
        from langchain import hub
        
        try:
            # Use ReAct agent for tool interaction
            react_prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, react_prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=15  # Increased iterations for comprehensive analysis
            )
            
            # Execute analysis
            print(f"📊 [Narrative Trend Analyst] Starting comprehensive market analysis...")
            start_time = time.time()
            
            response = agent_executor.invoke({
                "input": f"""Analyze the current US stock market narrative and trends as of {current_date}.

Provide a comprehensive market analysis including:

1. Current market narrative and driving forces
2. Long-term trend analysis and cycle positioning
3. Sector rotation and performance analysis
4. Key opportunities and risks

Then provide specific ticker recommendations:

BUY RECOMMENDATIONS (5-10 stocks):
- Stocks that align with current positive narratives
- Companies benefiting from current trends
- Undervalued opportunities in strong sectors

SELL/AVOID RECOMMENDATIONS (5-10 stocks):
- Stocks facing headwinds from current narratives
- Companies hurt by current trends
- Overvalued names in weak sectors

For each recommendation, provide ticker, company name, and detailed rationale based on the current market environment."""
            })
            
            end_time = time.time()
            print(f"📊 [Narrative Trend Analyst] Analysis completed in {end_time - start_time:.2f} seconds")
            
            # Extract the analysis result
            analysis_result = response.get("output", "No analysis result available")
            
            # Format the final report
            narrative_trend_report = f"""
# US Market Narrative & Trend Analysis Report
**Date:** {current_date}
**Analysis Type:** Comprehensive Market Narrative & Ticker Recommendations

## Market Analysis & Ticker Recommendations

{analysis_result}

---

## Key Takeaways
- **Market Focus:** Current narrative driving short-term movements
- **Trend Position:** Where we are in major market cycles
- **Opportunities:** Sectors and stocks positioned for growth
- **Risks:** Areas to avoid in current environment

---
*Report generated by Narrative Trend Analyst*
*Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*This analysis covers the overall US market without requiring specific ticker input*
"""
            
            print(f"📊 [Narrative Trend Analyst] Report generated successfully")
            print(f"📊 [DEBUG] Report length: {len(narrative_trend_report)} characters")
            
            return {
                "narrative_trend_report": narrative_trend_report,
                "messages": state.get("messages", []) + [AIMessage(content=narrative_trend_report)]
            }
            
        except Exception as e:
            print(f"❌ [Narrative Trend Analyst] Error during analysis: {e}")
            error_report = f"""
# US Market Narrative & Trend Analysis Report - Error
**Date:** {current_date}
**Status:** Analysis failed

Error occurred during narrative trend analysis: {str(e)}

Please check the configuration and try again.
"""
            return {
                "narrative_trend_report": error_report,
                "messages": state.get("messages", [])
            }
    
    return narrative_trend_analyst_node


class NarrativeTrendAnalyst:
    """
    Narrative Trend Analyst Class
    Provides methods for analyzing market narratives and trends
    Returns ticker recommendations based on market analysis
    """
    
    def __init__(self, llm, toolkit):
        self.llm = llm
        self.toolkit = toolkit
        self.analyst_node = create_narrative_trend_analyst(llm, toolkit)
    
    def analyze_market(self, trade_date: str = None) -> Dict[str, Any]:
        """
        Analyze overall market narrative and trends, provide ticker recommendations
        
        Args:
            trade_date: Analysis date (defaults to current date)
            
        Returns:
            Dict containing market analysis and ticker recommendations
        """
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y-%m-%d')
        
        state = {
            "trade_date": trade_date,
            "messages": []
        }
        
        return self.analyst_node(state)
    
    def get_market_narrative(self, date: str = None) -> Dict[str, Any]:
        """
        Get current market narrative and recommendations
        
        Args:
            date: Analysis date (defaults to current date)
            
        Returns:
            Dict containing market narrative analysis and ticker recommendations
        """
        return self.analyze_market(date)
    
    def get_buy_recommendations(self, date: str = None) -> Dict[str, Any]:
        """
        Get buy recommendations based on current market narrative
        
        Args:
            date: Analysis date (defaults to current date)
            
        Returns:
            Dict containing buy recommendations
        """
        analysis = self.analyze_market(date)
        
        # Extract buy recommendations from the full analysis
        # This would need to be enhanced to parse the actual recommendations
        return {
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'type': 'buy_recommendations',
            'analysis': analysis,
            'note': 'Buy recommendations are included in the full market analysis'
        }
    
    def get_sell_recommendations(self, date: str = None) -> Dict[str, Any]:
        """
        Get sell/avoid recommendations based on current market narrative
        
        Args:
            date: Analysis date (defaults to current date)
            
        Returns:
            Dict containing sell/avoid recommendations
        """
        analysis = self.analyze_market(date)
        
        # Extract sell recommendations from the full analysis
        # This would need to be enhanced to parse the actual recommendations
        return {
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'type': 'sell_recommendations',
            'analysis': analysis,
            'note': 'Sell recommendations are included in the full market analysis'
        }
    
    def get_sector_opportunities(self, date: str = None) -> Dict[str, Any]:
        """
        Get sector-based opportunities from market narrative
        
        Args:
            date: Analysis date (defaults to current date)
            
        Returns:
            Dict containing sector opportunities
        """
        analysis = self.analyze_market(date)
        
        return {
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'type': 'sector_opportunities',
            'analysis': analysis,
            'note': 'Sector opportunities are included in the full market analysis'
        } 