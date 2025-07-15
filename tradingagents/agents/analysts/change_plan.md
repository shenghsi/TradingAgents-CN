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

9. **System Integration:**
   - [ ] Add narrative trend analyst import to `tradingagents/agents/__init__.py`
   - [ ] Update `create_narrative_trend_analyst` function export in agents module
   - [ ] Integrate with existing TradingAgentsGraph workflow
   - [ ] Add to available analysts list in graph propagation logic

10. **Web Interface Integration:**
    - [ ] Add "叙述趋势分析师" option to Web interface analyst selection
    - [ ] Create dedicated "市场概览" page in Web interface for ticker-free analysis
    - [ ] Update `web/components/analysis_form.py` to include new analyst option
    - [ ] Add market overview functionality to sidebar navigation

11. **CLI Interface Integration:**
    - [ ] Add narrative trend analyst to CLI analyst selection options
    - [ ] Create "market-overview" command for ticker-free analysis
    - [ ] Update CLI help documentation to include new analyst
    - [ ] Add usage examples in CLI welcome messages

12. **Testing and Validation (Comprehensive):**
    - [ ] Create `test_narrative_trend_analyst.py` with comprehensive unit tests
    - [ ] Test integration with existing analyst workflow
    - [ ] Validate ticker-free analysis functionality
    - [ ] Test Web interface integration
    - [ ] Test CLI interface integration
    - [ ] Performance testing for data fetching and processing

13. **Documentation Updates:**
     - [ ] Update main README.md to include narrative trend analyst
     - [ ] Add usage guide for ticker-free market analysis
     - [ ] Update Web interface documentation
     - [ ] Update CLI documentation with new commands
     - [ ] Add examples in `examples/` directory

---

## CURRENT STATUS

### ✅ **COMPLETED (Phase 1)**
- Core analyst implementation with `NarrativeTrendAnalyst` class
- Data collection utilities (`investment_data_utils.py`, `trend_analysis_utils.py`)
- Market analysis functionality working without ticker input
- Buy/sell recommendations based on market narrative
- Basic testing and documentation

### 🔄 **IN PROGRESS (Phase 2)**
- System integration tasks (Items 9-13)
- User interface integration (Web and CLI)
- Comprehensive testing and validation
- Complete documentation updates

### 🎯 **NEXT STEPS**
1. **Priority 1**: Complete system integration (Item 9)
2. **Priority 2**: Add Web interface options (Item 10)
3. **Priority 3**: Update CLI interface (Item 11)
4. **Priority 4**: Comprehensive testing (Item 12)
5. **Priority 5**: Documentation updates (Item 13)

### 📝 **NOTES**
- The core functionality is implemented and working
- Main blocker is lack of integration with existing user interfaces
- Users cannot currently access the new analyst through standard workflows
- Need to create ticker-free analysis entry points in both Web and CLI