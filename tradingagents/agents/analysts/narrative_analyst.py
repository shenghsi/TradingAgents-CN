"""
Narrative Analyst - US Stock Market
Analyzes short-term market narrative/focus and long-term trends
Provides ticker recommendations based on market analysis
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


def create_narrative_analyst(llm, toolkit):
    """Create narrative analyst for US stock market"""
    
    def narrative_analyst_node(state):
        print(f"📊 [DEBUG] ===== Narrative Analyst Node Started =====")
        
        current_date = state["trade_date"]
        
        print(f"📊 [DEBUG] Input parameters: date={current_date}")
        print(f"📊 [DEBUG] Current state messages count: {len(state.get('messages', []))}")
        print(f"📊 [DEBUG] Existing narrative report: {state.get('narrative_report', 'None')[:100]}...")
        
        print(f"📊 [Narrative Analyst] Analyzing overall US market narrative and trends")
        print(f"📊 [DEBUG] Tool configuration check: online_tools={toolkit.config['online_tools']}")
        
        # Select tools based on configuration
        if toolkit.config["online_tools"]:
            # Use online tools for real-time data
            tools = [
                toolkit.get_realtime_stock_news,
                toolkit.get_global_news_openai,
                toolkit.get_google_news
            ]
            print(f"📊 [Narrative Analyst] Using online tools for real-time analysis")
        else:
            # Use cached/offline tools
            tools = [
                toolkit.get_finnhub_news,
                toolkit.get_reddit_news,
                toolkit.get_google_news
            ]
            print(f"📊 [Narrative Analyst] Using offline/cached tools")
        
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
        
        # Create system prompt for narrative analysis
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
            (
                "system",
                "您是一位有用的AI助手，与其他助手协作。"
                " 使用提供的工具来推进回答问题。"
                " 如果您无法完全回答，没关系；具有不同工具的其他助手"
                " 将从您停下的地方继续帮助。执行您能做的以取得进展。"
                " 如果您或任何其他助手有最终交易提案：**买入/持有/卖出**或可交付成果，"
                " 请在您的回应前加上最终交易提案：**买入/持有/卖出**，以便团队知道停止。"
                " 您可以访问以下工具：{tool_names}。\n{system_message}"
                "供您参考，当前日期是{current_date}。请用中文撰写所有分析内容。",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "human", 
                f"""Analyze the current US stock market narrative and trends as of {current_date}.

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

Use the available tools to gather the latest market data, news, and sentiment indicators to support your analysis."""
            )
        ])
        
        # 安全地获取工具名称，处理函数和工具对象
        tool_names = []
        for tool in tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            elif hasattr(tool, '__name__'):
                tool_names.append(tool.__name__)
            else:
                tool_names.append(str(tool))
        
        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join(tool_names))
        prompt = prompt.partial(current_date=current_date)
        
        try:
            # 使用与新闻分析师相同的LangChain工具调用机制
            print(f"📊 [Narrative Analyst] Starting comprehensive market analysis using LangChain tools...")
            start_time = time.time()
            
            # 使用 bind_tools 机制，与新闻分析师保持一致
            chain = prompt | llm.bind_tools(tools)
            result = chain.invoke(state["messages"])
            
            end_time = time.time()
            print(f"📊 [Narrative Analyst] Analysis completed in {end_time - start_time:.2f} seconds")
            
            # 检查工具调用
            if len(result.tool_calls) == 0:
                # 没有工具调用，直接使用LLM的回复
                analysis_result = result.content
                print(f"📊 [Narrative Analyst] 直接回复，长度: {len(analysis_result)}")
            else:
                # 有工具调用，执行工具并生成完整分析报告
                print(f"📊 [Narrative Analyst] 工具调用: {[call.get('name', 'unknown') for call in result.tool_calls]}")
                
                # 执行工具调用
                from langchain_core.messages import ToolMessage, HumanMessage
                
                tool_messages = []
                for tool_call in result.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_args = tool_call.get('args', {})
                    tool_id = tool_call.get('id')
                    
                    print(f"📊 [DEBUG] 执行工具: {tool_name}, 参数: {tool_args}")
                    
                    # 找到对应的工具并执行
                    tool_result = None
                    for tool in tools:
                        if hasattr(tool, 'name') and tool.name == tool_name:
                            try:
                                tool_result = tool.invoke(tool_args)
                                break
                            except Exception as e:
                                print(f"❌ [DEBUG] 工具执行失败: {tool_name} - {e}")
                                tool_result = f"工具执行失败: {str(e)}"
                                break
                        elif hasattr(tool, '__name__') and tool.__name__ == tool_name:
                            try:
                                tool_result = tool(**tool_args)
                                break
                            except Exception as e:
                                print(f"❌ [DEBUG] 工具执行失败: {tool_name} - {e}")
                                tool_result = f"工具执行失败: {str(e)}"
                                break
                    
                    if tool_result is None:
                        tool_result = f"未找到工具: {tool_name}"
                    
                    tool_messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))
                
                # 将工具结果发送给LLM进行最终分析
                final_messages = state["messages"] + [result] + tool_messages
                final_result = llm.invoke(final_messages)
                analysis_result = final_result.content
            
            # Format the final report
            narrative_report = f"""
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
*Report generated by Narrative Analyst*
*Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*This analysis covers the overall US market without requiring specific ticker input*
"""
            
            print(f"📊 [Narrative Analyst] Report generated successfully")
            print(f"📊 [DEBUG] Report length: {len(narrative_report)} characters")
            
            return {
                "narrative_report": narrative_report,
                "messages": state.get("messages", []) + [AIMessage(content=narrative_report)]
            }
            
        except Exception as e:
            print(f"❌ [Narrative Analyst] Error during analysis: {e}")
            error_report = f"""
# US Market Narrative Analysis Report - Error
**Date:** {current_date}
**Status:** Analysis failed

Error occurred during narrative analysis: {str(e)}

Please check the configuration and try again.
"""
            return {
                "narrative_report": error_report,
                "messages": state.get("messages", [])
            }
    
    return narrative_analyst_node


class NarrativeAnalyst:
    """
    Narrative Analyst Class
    Provides methods for analyzing market narratives and trends
    Returns ticker recommendations based on market analysis
    """
    
    def __init__(self, llm, toolkit):
        self.llm = llm
        self.toolkit = toolkit
        self.analyst_node = create_narrative_analyst(llm, toolkit)
    
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