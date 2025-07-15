"""
Investment Data Utilities
Fetches data on investments, acquisitions, and institutional flows using free APIs
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
from pathlib import Path
import os


class InvestmentDataUtils:
    """Utilities for fetching investment and acquisition data"""
    
    def __init__(self, cache_dir: str = None):
        """
        Initialize investment data utilities
        
        Args:
            cache_dir: Directory for caching data
        """
        if cache_dir is None:
            cache_dir = os.path.join(os.path.expanduser("~"), "Documents", "TradingAgents", "data", "cache")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_institutional_holdings(self, ticker: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get institutional holdings data for a ticker
        
        Args:
            ticker: Stock ticker symbol
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing institutional holdings data
        """
        cache_file = self.cache_dir / f"institutional_holdings_{ticker}.json"
        
        # Check cache first
        if use_cache and cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 3600:  # Cache for 1 hour
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Use Yahoo Finance API for institutional holdings
            url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
            params = {
                'modules': 'institutionOwnership,fundOwnership,majorHoldersBreakdown'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            result = data.get('quoteSummary', {}).get('result', [])
            
            if result:
                holdings_data = {
                    'ticker': ticker,
                    'timestamp': datetime.now().isoformat(),
                    'institutional_ownership': result[0].get('institutionOwnership', {}),
                    'fund_ownership': result[0].get('fundOwnership', {}),
                    'major_holders': result[0].get('majorHoldersBreakdown', {})
                }
                
                # Cache the result
                with open(cache_file, 'w') as f:
                    json.dump(holdings_data, f, indent=2)
                
                return holdings_data
            
        except Exception as e:
            print(f"❌ Error fetching institutional holdings for {ticker}: {e}")
        
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'error': 'Failed to fetch institutional holdings data'
        }
    
    def get_insider_transactions(self, ticker: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get insider transaction data for a ticker
        
        Args:
            ticker: Stock ticker symbol
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing insider transaction data
        """
        cache_file = self.cache_dir / f"insider_transactions_{ticker}.json"
        
        # Check cache first
        if use_cache and cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 3600:  # Cache for 1 hour
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Use Yahoo Finance API for insider transactions
            url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
            params = {
                'modules': 'insiderTransactions,insiderHolders,netSharePurchaseActivity'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            result = data.get('quoteSummary', {}).get('result', [])
            
            if result:
                insider_data = {
                    'ticker': ticker,
                    'timestamp': datetime.now().isoformat(),
                    'insider_transactions': result[0].get('insiderTransactions', {}),
                    'insider_holders': result[0].get('insiderHolders', {}),
                    'net_share_purchase_activity': result[0].get('netSharePurchaseActivity', {})
                }
                
                # Cache the result
                with open(cache_file, 'w') as f:
                    json.dump(insider_data, f, indent=2)
                
                return insider_data
            
        except Exception as e:
            print(f"❌ Error fetching insider transactions for {ticker}: {e}")
        
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'error': 'Failed to fetch insider transaction data'
        }
    
    def get_etf_flows(self, ticker: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get ETF flow data for a ticker or ETF
        
        Args:
            ticker: Stock ticker symbol or ETF symbol
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing ETF flow data
        """
        cache_file = self.cache_dir / f"etf_flows_{ticker}.json"
        
        # Check cache first
        if use_cache and cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 1800:  # Cache for 30 minutes
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Use Yahoo Finance API for fund profile data
            url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
            params = {
                'modules': 'fundProfile,topHoldings,fundPerformance'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            result = data.get('quoteSummary', {}).get('result', [])
            
            if result:
                etf_data = {
                    'ticker': ticker,
                    'timestamp': datetime.now().isoformat(),
                    'fund_profile': result[0].get('fundProfile', {}),
                    'top_holdings': result[0].get('topHoldings', {}),
                    'fund_performance': result[0].get('fundPerformance', {})
                }
                
                # Cache the result
                with open(cache_file, 'w') as f:
                    json.dump(etf_data, f, indent=2)
                
                return etf_data
            
        except Exception as e:
            print(f"❌ Error fetching ETF flows for {ticker}: {e}")
        
        return {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'error': 'Failed to fetch ETF flow data'
        }
    
    def get_sector_performance(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get sector performance data
        
        Args:
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing sector performance data
        """
        cache_file = self.cache_dir / "sector_performance.json"
        
        # Check cache first
        if use_cache and cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 900:  # Cache for 15 minutes
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Get sector ETF performance
            sector_etfs = {
                'Technology': 'XLK',
                'Healthcare': 'XLV',
                'Financial': 'XLF',
                'Consumer Discretionary': 'XLY',
                'Communication': 'XLC',
                'Industrial': 'XLI',
                'Consumer Staples': 'XLP',
                'Energy': 'XLE',
                'Utilities': 'XLU',
                'Real Estate': 'XLRE',
                'Materials': 'XLB'
            }
            
            sector_data = {}
            
            for sector, etf in sector_etfs.items():
                try:
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{etf}"
                    params = {
                        'range': '1mo',
                        'interval': '1d'
                    }
                    
                    response = self.session.get(url, params=params, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    chart = data.get('chart', {}).get('result', [])
                    
                    if chart:
                        meta = chart[0].get('meta', {})
                        sector_data[sector] = {
                            'symbol': etf,
                            'current_price': meta.get('regularMarketPrice'),
                            'previous_close': meta.get('previousClose'),
                            'change_percent': ((meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0)) / meta.get('previousClose', 1)) * 100,
                            'volume': meta.get('regularMarketVolume'),
                            'market_cap': meta.get('marketCap')
                        }
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    print(f"❌ Error fetching data for {sector} ({etf}): {e}")
                    continue
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'sectors': sector_data
            }
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            print(f"❌ Error fetching sector performance: {e}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'error': 'Failed to fetch sector performance data'
        }
    
    def get_market_movers(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get market movers (gainers and losers)
        
        Args:
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing market movers data
        """
        cache_file = self.cache_dir / "market_movers.json"
        
        # Check cache first
        if use_cache and cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 300:  # Cache for 5 minutes
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Get market movers from Yahoo Finance screener
            screener_url = "https://query1.finance.yahoo.com/v1/finance/screener"
            
            # Top gainers
            gainers_payload = {
                "size": 25,
                "offset": 0,
                "sortField": "percentchange",
                "sortType": "DESC",
                "quoteType": "EQUITY",
                "query": {
                    "operator": "AND",
                    "operands": [
                        {"operator": "GT", "operands": ["marketcap", 1000000000]},
                        {"operator": "GT", "operands": ["volume", 100000]}
                    ]
                }
            }
            
            # Top losers
            losers_payload = {
                "size": 25,
                "offset": 0,
                "sortField": "percentchange",
                "sortType": "ASC",
                "quoteType": "EQUITY",
                "query": {
                    "operator": "AND",
                    "operands": [
                        {"operator": "GT", "operands": ["marketcap", 1000000000]},
                        {"operator": "GT", "operands": ["volume", 100000]}
                    ]
                }
            }
            
            gainers_response = self.session.post(screener_url, json=gainers_payload, timeout=10)
            losers_response = self.session.post(screener_url, json=losers_payload, timeout=10)
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'gainers': [],
                'losers': []
            }
            
            if gainers_response.status_code == 200:
                gainers_data = gainers_response.json()
                quotes = gainers_data.get('finance', {}).get('result', [{}])[0].get('quotes', [])
                result['gainers'] = [
                    {
                        'symbol': quote.get('symbol'),
                        'shortName': quote.get('shortName'),
                        'regularMarketPrice': quote.get('regularMarketPrice'),
                        'regularMarketChange': quote.get('regularMarketChange'),
                        'regularMarketChangePercent': quote.get('regularMarketChangePercent'),
                        'regularMarketVolume': quote.get('regularMarketVolume'),
                        'marketCap': quote.get('marketCap')
                    }
                    for quote in quotes[:10]  # Top 10 gainers
                ]
            
            if losers_response.status_code == 200:
                losers_data = losers_response.json()
                quotes = losers_data.get('finance', {}).get('result', [{}])[0].get('quotes', [])
                result['losers'] = [
                    {
                        'symbol': quote.get('symbol'),
                        'shortName': quote.get('shortName'),
                        'regularMarketPrice': quote.get('regularMarketPrice'),
                        'regularMarketChange': quote.get('regularMarketChange'),
                        'regularMarketChangePercent': quote.get('regularMarketChangePercent'),
                        'regularMarketVolume': quote.get('regularMarketVolume'),
                        'marketCap': quote.get('marketCap')
                    }
                    for quote in quotes[:10]  # Top 10 losers
                ]
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            print(f"❌ Error fetching market movers: {e}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'error': 'Failed to fetch market movers data'
        }
    
    def get_earnings_calendar(self, days_ahead: int = 7, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get earnings calendar for upcoming days
        
        Args:
            days_ahead: Number of days to look ahead
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing earnings calendar data
        """
        cache_file = self.cache_dir / f"earnings_calendar_{days_ahead}d.json"
        
        # Check cache first
        if use_cache and cache_file.exists():
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age < 3600:  # Cache for 1 hour
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except:
                    pass
        
        try:
            # Use Yahoo Finance earnings calendar
            end_date = datetime.now() + timedelta(days=days_ahead)
            
            url = "https://query1.finance.yahoo.com/v1/finance/calendar/earnings"
            params = {
                'from': datetime.now().strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'size': 100
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            earnings_data = data.get('earnings', {}).get('result', [])
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'period': f"{datetime.now().strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                'earnings': []
            }
            
            for earning in earnings_data:
                result['earnings'].append({
                    'symbol': earning.get('ticker'),
                    'companyName': earning.get('companyshortname'),
                    'earningsDate': earning.get('startdatetime'),
                    'epsEstimate': earning.get('epsestimate'),
                    'epsActual': earning.get('epsactual'),
                    'revenueEstimate': earning.get('revenueestimate'),
                    'revenueActual': earning.get('revenueactual')
                })
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            return result
            
        except Exception as e:
            print(f"❌ Error fetching earnings calendar: {e}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'error': 'Failed to fetch earnings calendar data'
        }
    
    def analyze_investment_flows(self, ticker: str) -> Dict[str, Any]:
        """
        Analyze investment flows for a ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dict containing investment flow analysis
        """
        try:
            # Gather all investment data
            institutional_data = self.get_institutional_holdings(ticker)
            insider_data = self.get_insider_transactions(ticker)
            
            # Analyze the data
            analysis = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'institutional_sentiment': 'neutral',
                'insider_sentiment': 'neutral',
                'flow_summary': 'No significant flows detected',
                'key_insights': []
            }
            
            # Analyze institutional holdings
            if 'institutional_ownership' in institutional_data:
                inst_ownership = institutional_data['institutional_ownership']
                if 'ownershipList' in inst_ownership:
                    total_shares = sum(holding.get('position', {}).get('raw', 0) for holding in inst_ownership['ownershipList'])
                    if total_shares > 0:
                        analysis['institutional_sentiment'] = 'positive'
                        analysis['key_insights'].append(f"Strong institutional ownership with {len(inst_ownership['ownershipList'])} major holders")
            
            # Analyze insider transactions
            if 'insider_transactions' in insider_data:
                insider_trans = insider_data['insider_transactions']
                if 'transactions' in insider_trans:
                    buy_transactions = sum(1 for trans in insider_trans['transactions'] if trans.get('transactionText', '').lower().find('buy') >= 0)
                    sell_transactions = sum(1 for trans in insider_trans['transactions'] if trans.get('transactionText', '').lower().find('sell') >= 0)
                    
                    if buy_transactions > sell_transactions:
                        analysis['insider_sentiment'] = 'positive'
                        analysis['key_insights'].append(f"Insider buying activity: {buy_transactions} buy vs {sell_transactions} sell transactions")
                    elif sell_transactions > buy_transactions:
                        analysis['insider_sentiment'] = 'negative'
                        analysis['key_insights'].append(f"Insider selling activity: {sell_transactions} sell vs {buy_transactions} buy transactions")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing investment flows for {ticker}: {e}")
            return {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'error': 'Failed to analyze investment flows'
            } 