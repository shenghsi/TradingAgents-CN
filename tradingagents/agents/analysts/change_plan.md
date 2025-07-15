### CHANGE PLAN

**Objective:** Develop a new analyst focused on analyzing the short-term narrative/focus and long-term trends of the current US stock market, leveraging insights from top companies and VCs investments, acquisitions, and major market trends using free data sources. **The analyst works WITHOUT ticker input and provides specific buy/sell recommendations based on market analysis.**

#### Files to be Modified or Created:
- `tradingagents/agents/analysts/narrative_trend_analyst.py` (New)
- `tradingagents/dataflows/investment_data_utils.py` (New)
- `tradingagents/dataflows/trend_analysis_utils.py` (New)
- `tradingagents/config/api_keys.py` (Update for new API keys)

#### Rationale:
The new analyst will provide insights into the current market narrative and trends by analyzing data from top financial media, upcoming financial events, sector performance, and investment activities of top companies and VCs. This will help in identifying the driving forces behind market movements and provide actionable insights for investors.

### IMPLEMENTATION CHECKLIST

1. **Create New Analyst Class:**
   - [x] Create `narrative_trend_analyst.py` in the analysts directory.
   - [x] Implement a class `NarrativeTrendAnalyst` with methods for data collection, analysis, and report generation.

2. **Data Collection:**
   - [x] Develop `investment_data_utils.py` to fetch data on investments and acquisitions using free APIs like Yahoo Finance and Google Finance.
   - [x] Develop `trend_analysis_utils.py` to analyze trends using Google Trends API and free industry reports.

3. **API Integration:**
   - [x] Update `api_keys.py` to include API keys for new data sources (Google Trends). *Note: API keys are managed through config_manager.py*
   - [x] Implement API clients in `investment_data_utils.py` and `trend_analysis_utils.py`.

4. **Data Processing:**
   - [x] Implement data processing pipelines in `investment_data_utils.py` to clean and analyze investment data.
   - [x] Use NLP tools in `trend_analysis_utils.py` to process industry reports and news articles.

5. **Trend Analysis:**
   - [x] Implement time series analysis in `trend_analysis_utils.py` using libraries like Prophet or ARIMA.
   - [x] Develop methods to identify the current position in the trend cycle.

6. **Report Generation:**
   - [x] Define report templates in `narrative_trend_analyst.py` to present findings on market narrative, trends, and investment recommendations.
   - [x] Ensure reports include sections for short-term narrative/focus, long-term trend analysis, and stock recommendations.

7. **Testing and Validation:**
   - [x] Conduct unit tests for data fetching and processing functions.
   - [x] Validate the accuracy and reliability of the generated reports.

8. **Documentation:**
   - [x] Update project documentation to include details about the new analyst and its capabilities.
   - [x] Provide usage examples and API documentation for new utilities.