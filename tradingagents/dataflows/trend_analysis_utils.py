"""
Trend Analysis Utilities
Analyzes trends using Google Trends API and free industry reports
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
from pathlib import Path
import os
import re
from urllib.parse import quote


class TrendAnalysisUtils:
    """Utilities for analyzing market trends and cycles"""
    
    def __init__(self, cache_dir: str = None):
        """
        Initialize trend analysis utilities
        
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
        
        # Google Trends endpoints
        self.trends_base_url = "https://trends.google.com/trends/api"
    
    def get_google_trends_data(self, keywords: List[str], timeframe: str = "today 3-m", 
                              geo: str = "US", use_cache: bool = True) -> Dict[str, Any]:
        """
        Get Google Trends data for keywords
        
        Args:
            keywords: List of keywords to search
            timeframe: Time range (e.g., "today 3-m", "today 12-m")
            geo: Geographic location (default: US)
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing trends data
        """
        cache_key = f"trends_{'_'.join(keywords)}_{timeframe}_{geo}".replace(' ', '_')
        cache_file = self.cache_dir / f"{cache_key}.json"
        
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
            # Use pytrends-like approach for Google Trends
            # Note: This is a simplified implementation for demo purposes
            # In production, you would use the official pytrends library
            
            trends_data = {
                'keywords': keywords,
                'timeframe': timeframe,
                'geo': geo,
                'timestamp': datetime.now().isoformat(),
                'interest_over_time': [],
                'related_queries': {},
                'error': None
            }
            
            # For now, return mock data structure
            # In production, implement actual Google Trends API calls
            trends_data['interest_over_time'] = [
                {
                    'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                    'values': {kw: max(0, 50 + (i % 30) - 15) for kw in keywords}
                }
                for i in range(90, 0, -1)  # Last 90 days
            ]
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(trends_data, f, indent=2)
            
            return trends_data
            
        except Exception as e:
            print(f"❌ Error fetching Google Trends data: {e}")
            return {
                'keywords': keywords,
                'timeframe': timeframe,
                'geo': geo,
                'timestamp': datetime.now().isoformat(),
                'error': f'Failed to fetch trends data: {str(e)}'
            }
    
    def analyze_market_cycles(self, ticker: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Analyze market cycles for a ticker
        
        Args:
            ticker: Stock ticker symbol
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing cycle analysis
        """
        cache_file = self.cache_dir / f"market_cycles_{ticker}.json"
        
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
            # Get historical price data for cycle analysis
            price_data = self._get_historical_prices(ticker, period="2y")
            
            if not price_data or 'error' in price_data:
                return {
                    'ticker': ticker,
                    'timestamp': datetime.now().isoformat(),
                    'error': 'Failed to fetch price data for cycle analysis'
                }
            
            # Analyze cycles
            cycle_analysis = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'current_trend': 'neutral',
                'cycle_position': 'unknown',
                'support_levels': [],
                'resistance_levels': [],
                'trend_strength': 0,
                'volatility_analysis': {},
                'key_insights': []
            }
            
            prices = price_data.get('prices', [])
            if len(prices) >= 50:  # Need sufficient data for analysis
                
                # Calculate moving averages
                ma_20 = self._calculate_moving_average(prices, 20)
                ma_50 = self._calculate_moving_average(prices, 50)
                ma_200 = self._calculate_moving_average(prices, 200)
                
                current_price = prices[-1]['close']
                
                # Determine trend
                if current_price > ma_20 > ma_50 > ma_200:
                    cycle_analysis['current_trend'] = 'strong_uptrend'
                    cycle_analysis['trend_strength'] = 0.8
                elif current_price > ma_20 > ma_50:
                    cycle_analysis['current_trend'] = 'uptrend'
                    cycle_analysis['trend_strength'] = 0.6
                elif current_price < ma_20 < ma_50 < ma_200:
                    cycle_analysis['current_trend'] = 'strong_downtrend'
                    cycle_analysis['trend_strength'] = -0.8
                elif current_price < ma_20 < ma_50:
                    cycle_analysis['current_trend'] = 'downtrend'
                    cycle_analysis['trend_strength'] = -0.6
                else:
                    cycle_analysis['current_trend'] = 'sideways'
                    cycle_analysis['trend_strength'] = 0.1
                
                # Determine cycle position
                if current_price > ma_200:
                    cycle_analysis['cycle_position'] = 'above_long_term_average'
                else:
                    cycle_analysis['cycle_position'] = 'below_long_term_average'
                
                # Calculate support and resistance levels
                recent_prices = [p['close'] for p in prices[-60:]]  # Last 60 days
                cycle_analysis['support_levels'] = self._find_support_levels(recent_prices)
                cycle_analysis['resistance_levels'] = self._find_resistance_levels(recent_prices)
                
                # Volatility analysis
                returns = [(prices[i]['close'] - prices[i-1]['close']) / prices[i-1]['close'] 
                          for i in range(1, len(prices))]
                volatility = pd.Series(returns).std() * (252 ** 0.5)  # Annualized volatility
                
                cycle_analysis['volatility_analysis'] = {
                    'current_volatility': volatility,
                    'volatility_level': 'high' if volatility > 0.3 else 'medium' if volatility > 0.15 else 'low'
                }
                
                # Generate insights
                cycle_analysis['key_insights'] = self._generate_cycle_insights(cycle_analysis, current_price, ma_20, ma_50, ma_200)
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(cycle_analysis, f, indent=2)
            
            return cycle_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing market cycles for {ticker}: {e}")
            return {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'error': f'Failed to analyze market cycles: {str(e)}'
            }
    
    def get_economic_indicators(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get key economic indicators
        
        Args:
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing economic indicators
        """
        cache_file = self.cache_dir / "economic_indicators.json"
        
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
            # Get economic data from FRED API (free)
            indicators = {
                'timestamp': datetime.now().isoformat(),
                'fed_funds_rate': None,
                'unemployment_rate': None,
                'inflation_rate': None,
                'gdp_growth': None,
                'vix': None,
                'yield_curve': {},
                'error': None
            }
            
            # For demo purposes, we'll use mock data
            # In production, integrate with FRED API or similar free economic data sources
            indicators.update({
                'fed_funds_rate': 5.25,  # Mock current fed funds rate
                'unemployment_rate': 3.7,  # Mock unemployment rate
                'inflation_rate': 3.2,  # Mock inflation rate
                'gdp_growth': 2.1,  # Mock GDP growth
                'vix': 18.5,  # Mock VIX level
                'yield_curve': {
                    '3m': 5.1,
                    '2y': 4.8,
                    '10y': 4.3,
                    '30y': 4.4
                }
            })
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(indicators, f, indent=2)
            
            return indicators
            
        except Exception as e:
            print(f"❌ Error fetching economic indicators: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': f'Failed to fetch economic indicators: {str(e)}'
            }
    
    def analyze_sector_rotation(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Analyze sector rotation patterns
        
        Args:
            use_cache: Whether to use cached data
            
        Returns:
            Dict containing sector rotation analysis
        """
        cache_file = self.cache_dir / "sector_rotation.json"
        
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
            # Get sector performance data
            from .investment_data_utils import InvestmentDataUtils
            investment_utils = InvestmentDataUtils(self.cache_dir)
            sector_data = investment_utils.get_sector_performance(use_cache=use_cache)
            
            if 'error' in sector_data:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'error': 'Failed to fetch sector data for rotation analysis'
                }
            
            # Analyze rotation patterns
            rotation_analysis = {
                'timestamp': datetime.now().isoformat(),
                'leading_sectors': [],
                'lagging_sectors': [],
                'rotation_phase': 'unknown',
                'economic_cycle_position': 'unknown',
                'key_insights': []
            }
            
            sectors = sector_data.get('sectors', {})
            if sectors:
                # Sort sectors by performance
                sector_performance = [
                    {
                        'sector': sector,
                        'performance': data.get('change_percent', 0),
                        'volume': data.get('volume', 0)
                    }
                    for sector, data in sectors.items()
                    if data.get('change_percent') is not None
                ]
                
                sector_performance.sort(key=lambda x: x['performance'], reverse=True)
                
                # Identify leading and lagging sectors
                rotation_analysis['leading_sectors'] = sector_performance[:3]
                rotation_analysis['lagging_sectors'] = sector_performance[-3:]
                
                # Determine rotation phase based on sector performance
                tech_performance = next((s['performance'] for s in sector_performance if s['sector'] == 'Technology'), 0)
                financial_performance = next((s['performance'] for s in sector_performance if s['sector'] == 'Financial'), 0)
                defensive_performance = sum(s['performance'] for s in sector_performance 
                                          if s['sector'] in ['Utilities', 'Consumer Staples', 'Healthcare']) / 3
                
                if tech_performance > financial_performance > defensive_performance:
                    rotation_analysis['rotation_phase'] = 'growth_phase'
                    rotation_analysis['economic_cycle_position'] = 'expansion'
                elif financial_performance > tech_performance > defensive_performance:
                    rotation_analysis['rotation_phase'] = 'value_phase'
                    rotation_analysis['economic_cycle_position'] = 'late_cycle'
                elif defensive_performance > tech_performance and defensive_performance > financial_performance:
                    rotation_analysis['rotation_phase'] = 'defensive_phase'
                    rotation_analysis['economic_cycle_position'] = 'recession_risk'
                else:
                    rotation_analysis['rotation_phase'] = 'mixed_signals'
                    rotation_analysis['economic_cycle_position'] = 'transition'
                
                # Generate insights
                rotation_analysis['key_insights'] = [
                    f"Leading sectors: {', '.join([s['sector'] for s in rotation_analysis['leading_sectors']])}",
                    f"Current rotation phase: {rotation_analysis['rotation_phase']}",
                    f"Economic cycle position: {rotation_analysis['economic_cycle_position']}"
                ]
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(rotation_analysis, f, indent=2)
            
            return rotation_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing sector rotation: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': f'Failed to analyze sector rotation: {str(e)}'
            }
    
    def _get_historical_prices(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """Get historical price data for a ticker"""
        try:
            # Use Yahoo Finance API for historical data
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                'range': period,
                'interval': '1d'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            chart = data.get('chart', {}).get('result', [])
            
            if chart:
                timestamps = chart[0].get('timestamp', [])
                quote = chart[0].get('indicators', {}).get('quote', [{}])[0]
                
                prices = []
                for i, timestamp in enumerate(timestamps):
                    if (quote.get('close', [])[i] is not None and 
                        quote.get('open', [])[i] is not None and
                        quote.get('high', [])[i] is not None and
                        quote.get('low', [])[i] is not None):
                        
                        prices.append({
                            'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                            'open': quote.get('open', [])[i],
                            'high': quote.get('high', [])[i],
                            'low': quote.get('low', [])[i],
                            'close': quote.get('close', [])[i],
                            'volume': quote.get('volume', [])[i] or 0
                        })
                
                return {
                    'ticker': ticker,
                    'period': period,
                    'prices': prices
                }
            
        except Exception as e:
            print(f"❌ Error fetching historical prices for {ticker}: {e}")
        
        return {
            'ticker': ticker,
            'period': period,
            'error': 'Failed to fetch historical price data'
        }
    
    def _calculate_moving_average(self, prices: List[Dict], window: int) -> float:
        """Calculate moving average for given window"""
        if len(prices) < window:
            return 0
        
        recent_prices = [p['close'] for p in prices[-window:]]
        return sum(recent_prices) / len(recent_prices)
    
    def _find_support_levels(self, prices: List[float]) -> List[float]:
        """Find support levels from price data"""
        if len(prices) < 10:
            return []
        
        # Simple support level detection
        support_levels = []
        for i in range(2, len(prices) - 2):
            if (prices[i] < prices[i-1] and prices[i] < prices[i+1] and
                prices[i] < prices[i-2] and prices[i] < prices[i+2]):
                support_levels.append(prices[i])
        
        # Return unique support levels, sorted
        return sorted(list(set(support_levels)))[-3:]  # Last 3 support levels
    
    def _find_resistance_levels(self, prices: List[float]) -> List[float]:
        """Find resistance levels from price data"""
        if len(prices) < 10:
            return []
        
        # Simple resistance level detection
        resistance_levels = []
        for i in range(2, len(prices) - 2):
            if (prices[i] > prices[i-1] and prices[i] > prices[i+1] and
                prices[i] > prices[i-2] and prices[i] > prices[i+2]):
                resistance_levels.append(prices[i])
        
        # Return unique resistance levels, sorted
        return sorted(list(set(resistance_levels)))[-3:]  # Last 3 resistance levels
    
    def _generate_cycle_insights(self, analysis: Dict, current_price: float, 
                               ma_20: float, ma_50: float, ma_200: float) -> List[str]:
        """Generate insights from cycle analysis"""
        insights = []
        
        # Trend insights
        if analysis['current_trend'] == 'strong_uptrend':
            insights.append("Strong uptrend with price above all major moving averages")
        elif analysis['current_trend'] == 'strong_downtrend':
            insights.append("Strong downtrend with price below all major moving averages")
        elif analysis['current_trend'] == 'sideways':
            insights.append("Sideways trend with mixed signals from moving averages")
        
        # Cycle position insights
        if analysis['cycle_position'] == 'above_long_term_average':
            insights.append("Price trading above long-term average, suggesting bullish cycle")
        else:
            insights.append("Price trading below long-term average, suggesting bearish cycle")
        
        # Volatility insights
        vol_level = analysis['volatility_analysis'].get('volatility_level', 'medium')
        if vol_level == 'high':
            insights.append("High volatility indicates increased uncertainty and risk")
        elif vol_level == 'low':
            insights.append("Low volatility suggests stable market conditions")
        
        return insights 