import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')


def get_country_index_mapping() -> Dict[str, Dict[str, Any]]:
    return {
        "United States": {"index": "^GSPC", "currency": "USD", "currency_pair": None, "gdp_weight": 1.0, "tax_rate": 0.21, "ease_of_business": 0.84, "sectors": ["Technology", "Healthcare", "Finance"], "commodities": ["Oil", "Natural Gas", "Corn"]},
        "China": {"index": "000001.SS", "currency": "CNY", "currency_pair": "USDCNY=X", "gdp_weight": 0.85, "tax_rate": 0.25, "ease_of_business": 0.55, "sectors": ["Manufacturing", "Technology", "Renewable Energy"], "commodities": ["Rare Earths", "Steel", "Coal"]},
        "Japan": {"index": "^N225", "currency": "JPY", "currency_pair": "USDJPY=X", "gdp_weight": 0.65, "tax_rate": 0.234, "ease_of_business": 0.78, "sectors": ["Automotive", "Electronics", "Robotics"], "commodities": ["Electronics Components", "Machinery"]},
        "Germany": {"index": "^GDAXI", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.55, "tax_rate": 0.30, "ease_of_business": 0.79, "sectors": ["Automotive", "Engineering", "Chemicals"], "commodities": ["Machinery", "Vehicles", "Pharmaceuticals"]},
        "United Kingdom": {"index": "^FTSE", "currency": "GBP", "currency_pair": "GBPUSD=X", "gdp_weight": 0.45, "tax_rate": 0.25, "ease_of_business": 0.83, "sectors": ["Finance", "Pharmaceuticals", "Energy"], "commodities": ["Oil", "Financial Services"]},
        "India": {"index": "^BSESN", "currency": "INR", "currency_pair": "USDINR=X", "gdp_weight": 0.50, "tax_rate": 0.25, "ease_of_business": 0.63, "sectors": ["IT Services", "Pharmaceuticals", "Finance"], "commodities": ["IT Services", "Textiles", "Gems"]},
        "France": {"index": "^FCHI", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.40, "tax_rate": 0.25, "ease_of_business": 0.76, "sectors": ["Luxury Goods", "Aerospace", "Agriculture"], "commodities": ["Wine", "Aircraft", "Luxury Goods"]},
        "Italy": {"index": "FTSEMIB.MI", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.30, "tax_rate": 0.24, "ease_of_business": 0.72, "sectors": ["Fashion", "Automotive", "Machinery"], "commodities": ["Machinery", "Textiles", "Food Products"]},
        "Canada": {"index": "^GSPTSE", "currency": "CAD", "currency_pair": "USDCAD=X", "gdp_weight": 0.28, "tax_rate": 0.15, "ease_of_business": 0.80, "sectors": ["Energy", "Mining", "Finance"], "commodities": ["Oil", "Gold", "Lumber"]},
        "South Korea": {"index": "^KS11", "currency": "KRW", "currency_pair": "USDKRW=X", "gdp_weight": 0.26, "tax_rate": 0.25, "ease_of_business": 0.84, "sectors": ["Electronics", "Automotive", "Shipbuilding"], "commodities": ["Semiconductors", "Ships", "Electronics"]},
        "Brazil": {"index": "^BVSP", "currency": "BRL", "currency_pair": "USDBRL=X", "gdp_weight": 0.24, "tax_rate": 0.34, "ease_of_business": 0.59, "sectors": ["Agriculture", "Mining", "Energy"], "commodities": ["Soybeans", "Iron Ore", "Coffee"]},
        "Australia": {"index": "^AXJO", "currency": "AUD", "currency_pair": "AUDUSD=X", "gdp_weight": 0.22, "tax_rate": 0.30, "ease_of_business": 0.81, "sectors": ["Mining", "Finance", "Healthcare"], "commodities": ["Iron Ore", "Coal", "Gold"]},
        "Russia": {"index": "IMOEX.ME", "currency": "RUB", "currency_pair": "USDRUB=X", "gdp_weight": 0.25, "tax_rate": 0.20, "ease_of_business": 0.45, "sectors": ["Energy", "Mining", "Defense"], "commodities": ["Oil", "Natural Gas", "Palladium"]},
        "Spain": {"index": "^IBEX", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.20, "tax_rate": 0.25, "ease_of_business": 0.77, "sectors": ["Tourism", "Renewable Energy", "Agriculture"], "commodities": ["Olive Oil", "Wine", "Vehicles"]},
        "Mexico": {"index": "^MXX", "currency": "MXN", "currency_pair": "USDMXN=X", "gdp_weight": 0.18, "tax_rate": 0.30, "ease_of_business": 0.60, "sectors": ["Automotive", "Electronics", "Oil"], "commodities": ["Oil", "Vehicles", "Electronics"]},
        "Indonesia": {"index": "^JKSE", "currency": "IDR", "currency_pair": "USDIDR=X", "gdp_weight": 0.17, "tax_rate": 0.22, "ease_of_business": 0.69, "sectors": ["Commodities", "Finance", "Consumer Goods"], "commodities": ["Palm Oil", "Coal", "Rubber"]},
        "Netherlands": {"index": "^AEX", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.14, "tax_rate": 0.258, "ease_of_business": 0.82, "sectors": ["Logistics", "Agriculture", "Technology"], "commodities": ["Flowers", "Dairy", "Machinery"]},
        "Saudi Arabia": {"index": "^TASI", "currency": "SAR", "currency_pair": "USDSAR=X", "gdp_weight": 0.13, "tax_rate": 0.20, "ease_of_business": 0.62, "sectors": ["Energy", "Petrochemicals", "Finance"], "commodities": ["Oil", "Petrochemicals"]},
        "Turkey": {"index": "XU100.IS", "currency": "TRY", "currency_pair": "USDTRY=X", "gdp_weight": 0.12, "tax_rate": 0.25, "ease_of_business": 0.69, "sectors": ["Textiles", "Automotive", "Agriculture"], "commodities": ["Textiles", "Food Products", "Vehicles"]},
        "Switzerland": {"index": "^SSMI", "currency": "CHF", "currency_pair": "USDCHF=X", "gdp_weight": 0.11, "tax_rate": 0.085, "ease_of_business": 0.86, "sectors": ["Finance", "Pharmaceuticals", "Precision Instruments"], "commodities": ["Pharmaceuticals", "Watches", "Gold"]},
        "Poland": {"index": "^WIG20", "currency": "PLN", "currency_pair": "USDPLN=X", "gdp_weight": 0.09, "tax_rate": 0.19, "ease_of_business": 0.76, "sectors": ["Manufacturing", "IT", "Agriculture"], "commodities": ["Machinery", "Food Products", "Furniture"]},
        "Sweden": {"index": "^OMX", "currency": "SEK", "currency_pair": "USDSEK=X", "gdp_weight": 0.08, "tax_rate": 0.206, "ease_of_business": 0.82, "sectors": ["Technology", "Automotive", "Forestry"], "commodities": ["Vehicles", "Machinery", "Paper"]},
        "Belgium": {"index": "^BFX", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.07, "tax_rate": 0.25, "ease_of_business": 0.75, "sectors": ["Chemicals", "Pharmaceuticals", "Logistics"], "commodities": ["Diamonds", "Chemicals", "Machinery"]},
        "Argentina": {"index": "^MERV", "currency": "ARS", "currency_pair": "USDARS=X", "gdp_weight": 0.065, "tax_rate": 0.35, "ease_of_business": 0.45, "sectors": ["Agriculture", "Energy", "Mining"], "commodities": ["Soybeans", "Beef", "Lithium"]},
        "Thailand": {"index": "^SET.BK", "currency": "THB", "currency_pair": "USDTHB=X", "gdp_weight": 0.07, "tax_rate": 0.20, "ease_of_business": 0.71, "sectors": ["Tourism", "Electronics", "Automotive"], "commodities": ["Rice", "Rubber", "Electronics"]},
        "Austria": {"index": "^ATX", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.06, "tax_rate": 0.25, "ease_of_business": 0.78, "sectors": ["Tourism", "Machinery", "Steel"], "commodities": ["Machinery", "Vehicles", "Steel"]},
        "Norway": {"index": "^OSEAX", "currency": "NOK", "currency_pair": "USDNOK=X", "gdp_weight": 0.06, "tax_rate": 0.22, "ease_of_business": 0.82, "sectors": ["Energy", "Shipping", "Seafood"], "commodities": ["Oil", "Natural Gas", "Fish"]},
        "United Arab Emirates": {"index": "^DFMGI", "currency": "AED", "currency_pair": "USDAED=X", "gdp_weight": 0.055, "tax_rate": 0.09, "ease_of_business": 0.80, "sectors": ["Real Estate", "Finance", "Tourism"], "commodities": ["Oil", "Aluminum", "Gold"]},
        "Nigeria": {"index": "^NGSE", "currency": "NGN", "currency_pair": "USDNGN=X", "gdp_weight": 0.055, "tax_rate": 0.30, "ease_of_business": 0.52, "sectors": ["Oil", "Agriculture", "Telecommunications"], "commodities": ["Oil", "Cocoa", "Rubber"]},
        "Israel": {"index": "^TA125.TA", "currency": "ILS", "currency_pair": "USDILS=X", "gdp_weight": 0.052, "tax_rate": 0.23, "ease_of_business": 0.76, "sectors": ["Technology", "Defense", "Pharmaceuticals"], "commodities": ["Diamonds", "Technology", "Chemicals"]},
        "Ireland": {"index": "^ISEQ", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.05, "tax_rate": 0.125, "ease_of_business": 0.80, "sectors": ["Technology", "Pharmaceuticals", "Finance"], "commodities": ["Pharmaceuticals", "Computers", "Chemicals"]},
        "Hong Kong": {"index": "^HSI", "currency": "HKD", "currency_pair": "USDHKD=X", "gdp_weight": 0.05, "tax_rate": 0.165, "ease_of_business": 0.85, "sectors": ["Finance", "Real Estate", "Trade"], "commodities": ["Financial Services", "Electronics"]},
        "Singapore": {"index": "^STI", "currency": "SGD", "currency_pair": "USDSGD=X", "gdp_weight": 0.048, "tax_rate": 0.17, "ease_of_business": 0.86, "sectors": ["Finance", "Technology", "Logistics"], "commodities": ["Electronics", "Refined Petroleum", "Machinery"]},
        "Malaysia": {"index": "^KLSE", "currency": "MYR", "currency_pair": "USDMYR=X", "gdp_weight": 0.045, "tax_rate": 0.24, "ease_of_business": 0.73, "sectors": ["Electronics", "Palm Oil", "Petrochemicals"], "commodities": ["Palm Oil", "Rubber", "Electronics"]},
        "Philippines": {"index": "^PSEI", "currency": "PHP", "currency_pair": "USDPHP=X", "gdp_weight": 0.044, "tax_rate": 0.25, "ease_of_business": 0.62, "sectors": ["BPO", "Electronics", "Remittances"], "commodities": ["Electronics", "Coconut Products", "Copper"]},
        "South Africa": {"index": "^JN0U.JO", "currency": "ZAR", "currency_pair": "USDZAR=X", "gdp_weight": 0.043, "tax_rate": 0.27, "ease_of_business": 0.67, "sectors": ["Mining", "Finance", "Agriculture"], "commodities": ["Gold", "Platinum", "Coal"]},
        "Denmark": {"index": "^OMXC25", "currency": "DKK", "currency_pair": "USDDKK=X", "gdp_weight": 0.042, "tax_rate": 0.22, "ease_of_business": 0.85, "sectors": ["Pharmaceuticals", "Renewable Energy", "Shipping"], "commodities": ["Pharmaceuticals", "Machinery", "Food Products"]},
        "Colombia": {"index": "^COLCAP", "currency": "COP", "currency_pair": "USDCOP=X", "gdp_weight": 0.04, "tax_rate": 0.35, "ease_of_business": 0.60, "sectors": ["Oil", "Agriculture", "Mining"], "commodities": ["Coffee", "Oil", "Coal"]},
        "Egypt": {"index": "^CASE30", "currency": "EGP", "currency_pair": "USDEGP=X", "gdp_weight": 0.038, "tax_rate": 0.225, "ease_of_business": 0.55, "sectors": ["Tourism", "Energy", "Agriculture"], "commodities": ["Cotton", "Oil", "Natural Gas"]},
        "Finland": {"index": "^OMXH25", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.035, "tax_rate": 0.20, "ease_of_business": 0.80, "sectors": ["Technology", "Forestry", "Machinery"], "commodities": ["Paper", "Machinery", "Electronics"]},
        "Chile": {"index": "^SPCLXIGPA", "currency": "CLP", "currency_pair": "USDCLP=X", "gdp_weight": 0.035, "tax_rate": 0.27, "ease_of_business": 0.72, "sectors": ["Mining", "Agriculture", "Fisheries"], "commodities": ["Copper", "Lithium", "Wine"]},
        "Portugal": {"index": "^PSI20", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.032, "tax_rate": 0.21, "ease_of_business": 0.76, "sectors": ["Tourism", "Textiles", "Renewable Energy"], "commodities": ["Cork", "Wine", "Textiles"]},
        "Czech Republic": {"index": "^PX", "currency": "CZK", "currency_pair": "USDCZK=X", "gdp_weight": 0.032, "tax_rate": 0.19, "ease_of_business": 0.76, "sectors": ["Automotive", "Engineering", "IT"], "commodities": ["Vehicles", "Machinery", "Glass"]},
        "Vietnam": {"index": "^VNINDEX", "currency": "VND", "currency_pair": "USDVND=X", "gdp_weight": 0.03, "tax_rate": 0.20, "ease_of_business": 0.70, "sectors": ["Electronics", "Textiles", "Agriculture"], "commodities": ["Electronics", "Textiles", "Seafood"]},
        "New Zealand": {"index": "^NZ50", "currency": "NZD", "currency_pair": "NZDUSD=X", "gdp_weight": 0.028, "tax_rate": 0.28, "ease_of_business": 0.86, "sectors": ["Agriculture", "Tourism", "Technology"], "commodities": ["Dairy", "Meat", "Wine"]},
        "Greece": {"index": "^ATG", "currency": "EUR", "currency_pair": "EURUSD=X", "gdp_weight": 0.026, "tax_rate": 0.22, "ease_of_business": 0.68, "sectors": ["Tourism", "Shipping", "Agriculture"], "commodities": ["Olive Oil", "Shipping Services", "Pharmaceuticals"]},
        "Romania": {"index": "^BET", "currency": "RON", "currency_pair": "USDRON=X", "gdp_weight": 0.025, "tax_rate": 0.16, "ease_of_business": 0.73, "sectors": ["IT", "Automotive", "Agriculture"], "commodities": ["Machinery", "Vehicles", "Grain"]},
        "Pakistan": {"index": "^KSE100", "currency": "PKR", "currency_pair": "USDPKR=X", "gdp_weight": 0.024, "tax_rate": 0.29, "ease_of_business": 0.55, "sectors": ["Textiles", "Agriculture", "IT Services"], "commodities": ["Textiles", "Rice", "Leather"]},
        "Hungary": {"index": "^BUX", "currency": "HUF", "currency_pair": "USDHUF=X", "gdp_weight": 0.022, "tax_rate": 0.09, "ease_of_business": 0.73, "sectors": ["Automotive", "Electronics", "Pharmaceuticals"], "commodities": ["Vehicles", "Machinery", "Pharmaceuticals"]},
    }


def fetch_index_data(ticker: str, period: str = "5y") -> Optional[pd.DataFrame]:
    try:
        index = yf.Ticker(ticker)
        hist = index.history(period=period)
        if hist.empty:
            return None
        return hist
    except Exception:
        return None


def fetch_currency_data(pair: str, period: str = "1y") -> Optional[pd.DataFrame]:
    try:
        currency = yf.Ticker(pair)
        hist = currency.history(period=period)
        if hist.empty:
            return None
        return hist
    except Exception:
        return None


def calculate_returns(data: pd.DataFrame) -> Dict[str, float]:
    if data is None or len(data) < 2:
        return {"daily_return": 0.0, "total_return": 0.0, "annualized_return": 0.0}
    daily_returns = data['Close'].pct_change().dropna()
    total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1
    trading_days = len(data)
    years = trading_days / 252
    annualized_return = ((1 + total_return) ** (1 / years)) - 1 if years > 0 else 0
    return {"daily_return": daily_returns.mean() if len(daily_returns) > 0 else 0.0, "total_return": total_return, "annualized_return": annualized_return}


def calculate_volatility(data: pd.DataFrame) -> Dict[str, float]:
    if data is None or len(data) < 2:
        return {"daily_volatility": 0.0, "annualized_volatility": 0.0, "max_drawdown": 0.0}
    daily_returns = data['Close'].pct_change().dropna()
    daily_vol = daily_returns.std()
    annualized_vol = daily_vol * np.sqrt(252)
    rolling_max = data['Close'].expanding().max()
    drawdown = (data['Close'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    return {"daily_volatility": daily_vol, "annualized_volatility": annualized_vol, "max_drawdown": abs(max_drawdown)}


def calculate_momentum(data: pd.DataFrame) -> Dict[str, float]:
    if data is None or len(data) < 252:
        return {"momentum_1m": 0.0, "momentum_3m": 0.0, "momentum_6m": 0.0, "momentum_12m": 0.0}
    close = data['Close']
    momentum_1m = (close.iloc[-1] / close.iloc[-21]) - 1 if len(close) >= 21 else 0
    momentum_3m = (close.iloc[-1] / close.iloc[-63]) - 1 if len(close) >= 63 else 0
    momentum_6m = (close.iloc[-1] / close.iloc[-126]) - 1 if len(close) >= 126 else 0
    momentum_12m = (close.iloc[-1] / close.iloc[-252]) - 1 if len(close) >= 252 else 0
    return {"momentum_1m": momentum_1m, "momentum_3m": momentum_3m, "momentum_6m": momentum_6m, "momentum_12m": momentum_12m}


def calculate_risk_adjusted_returns(data: pd.DataFrame, risk_free_rate: float = 0.04) -> Dict[str, float]:
    if data is None or len(data) < 2:
        return {"sharpe_ratio": 0.0, "sortino_ratio": 0.0, "calmar_ratio": 0.0}
    daily_returns = data['Close'].pct_change().dropna()
    excess_returns = daily_returns - (risk_free_rate / 252)
    sharpe = (excess_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() > 0 else 0
    downside_returns = daily_returns[daily_returns < 0]
    downside_std = downside_returns.std() if len(downside_returns) > 0 else 0.0001
    sortino = (excess_returns.mean() / downside_std) * np.sqrt(252) if downside_std > 0 else 0
    rolling_max = data['Close'].expanding().max()
    drawdown = (data['Close'] - rolling_max) / rolling_max
    max_drawdown = abs(drawdown.min())
    annualized_return = daily_returns.mean() * 252
    calmar = annualized_return / max_drawdown if max_drawdown > 0 else 0
    return {"sharpe_ratio": sharpe, "sortino_ratio": sortino, "calmar_ratio": calmar}


def calculate_trend_strength(data: pd.DataFrame) -> Dict[str, float]:
    if data is None or len(data) < 200:
        return {"trend_score": 0.5, "above_sma_50": False, "above_sma_200": False, "golden_cross": False}
    close = data['Close']
    sma_50 = close.rolling(50).mean().iloc[-1]
    sma_200 = close.rolling(200).mean().iloc[-1]
    current_price = close.iloc[-1]
    above_sma_50 = current_price > sma_50
    above_sma_200 = current_price > sma_200
    golden_cross = sma_50 > sma_200
    trend_score = 0.5
    if above_sma_50:
        trend_score += 0.15
    if above_sma_200:
        trend_score += 0.15
    if golden_cross:
        trend_score += 0.20
    return {"trend_score": min(trend_score, 1.0), "above_sma_50": above_sma_50, "above_sma_200": above_sma_200, "golden_cross": golden_cross}


def calculate_currency_risk(currency_data: pd.DataFrame) -> Dict[str, float]:
    if currency_data is None or len(currency_data) < 2:
        return {"currency_volatility": 0.0, "currency_trend": 0.0, "currency_risk_score": 0.5}
    daily_returns = currency_data['Close'].pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252)
    trend = (currency_data['Close'].iloc[-1] / currency_data['Close'].iloc[0]) - 1 if len(currency_data) > 0 else 0
    risk_score = min(volatility * 2, 1.0)
    return {"currency_volatility": volatility, "currency_trend": trend, "currency_risk_score": risk_score}


def calculate_tax_drag_score(tax_rate: float) -> float:
    return max(0, 1 - (tax_rate / 0.5))


def calculate_market_liquidity_score(data: pd.DataFrame) -> float:
    if data is None or 'Volume' not in data.columns:
        return 0.5
    avg_volume = data['Volume'].mean()
    if avg_volume > 1e9:
        return 1.0
    elif avg_volume > 1e8:
        return 0.85
    elif avg_volume > 1e7:
        return 0.70
    elif avg_volume > 1e6:
        return 0.55
    else:
        return 0.40


def calculate_stability_score(volatility: float, max_drawdown: float) -> float:
    vol_score = max(0, 1 - (volatility / 0.5))
    dd_score = max(0, 1 - (max_drawdown / 0.6))
    return (vol_score * 0.5) + (dd_score * 0.5)


def calculate_growth_score(returns: Dict[str, float], momentum: Dict[str, float]) -> float:
    return_component = min(max((returns['annualized_return'] + 0.2) / 0.6, 0), 1)
    momentum_component = min(max((momentum['momentum_12m'] + 0.3) / 0.8, 0), 1)
    return (return_component * 0.6) + (momentum_component * 0.4)


def calculate_business_friendliness_score(country_info: Dict[str, Any], index_data: pd.DataFrame, currency_data: pd.DataFrame) -> Dict[str, float]:
    base_ease = country_info.get('ease_of_business', 0.5)
    tax_score = calculate_tax_drag_score(country_info.get('tax_rate', 0.25))
    liquidity_score = calculate_market_liquidity_score(index_data)
    volatility_metrics = calculate_volatility(index_data)
    stability_score = calculate_stability_score(volatility_metrics['annualized_volatility'], volatility_metrics['max_drawdown'])
    currency_risk = calculate_currency_risk(currency_data)
    currency_score = 1 - currency_risk['currency_risk_score']
    returns = calculate_returns(index_data)
    momentum = calculate_momentum(index_data)
    growth_score = calculate_growth_score(returns, momentum)
    weights = {"base_ease": 0.20, "tax_efficiency": 0.15, "market_liquidity": 0.15, "market_stability": 0.15, "currency_stability": 0.15, "growth_potential": 0.20}
    final_score = (base_ease * weights['base_ease'] + tax_score * weights['tax_efficiency'] + liquidity_score * weights['market_liquidity'] + stability_score * weights['market_stability'] + currency_score * weights['currency_stability'] + growth_score * weights['growth_potential'])
    return {"overall_score": round(final_score * 100, 2), "base_ease_of_business": round(base_ease * 100, 2), "tax_efficiency_score": round(tax_score * 100, 2), "market_liquidity_score": round(liquidity_score * 100, 2), "market_stability_score": round(stability_score * 100, 2), "currency_stability_score": round(currency_score * 100, 2), "growth_potential_score": round(growth_score * 100, 2)}


def estimate_gdp_growth_probability(index_data: pd.DataFrame, momentum: Dict[str, float], volatility: Dict[str, float]) -> Dict[str, float]:
    if index_data is None:
        return {"gdp_growth_probability": 50.0, "investment_growth_probability": 50.0}
    market_return_factor = min(max((momentum['momentum_12m'] + 0.2) / 0.5, 0), 1) * 30
    stability_factor = max(0, (0.4 - volatility['annualized_volatility']) / 0.4) * 20
    trend_metrics = calculate_trend_strength(index_data)
    trend_factor = trend_metrics['trend_score'] * 25
    momentum_factor = min(max((momentum['momentum_6m'] + 0.15) / 0.35, 0), 1) * 25
    gdp_probability = min(max(market_return_factor + stability_factor + trend_factor, 10), 95)
    investment_probability = min(max(market_return_factor + momentum_factor + trend_factor, 10), 95)
    return {"gdp_growth_probability": round(gdp_probability, 2), "investment_growth_probability": round(investment_probability, 2)}


def identify_growth_sectors(country_info: Dict[str, Any], momentum: Dict[str, float]) -> Dict[str, Any]:
    base_sectors = country_info.get('sectors', [])
    commodities = country_info.get('commodities', [])
    market_momentum = momentum.get('momentum_6m', 0)
    if market_momentum > 0.15:
        sector_outlook = "Strong Growth Expected"
        recommended_exposure = "High"
    elif market_momentum > 0.05:
        sector_outlook = "Moderate Growth Expected"
        recommended_exposure = "Medium"
    elif market_momentum > -0.05:
        sector_outlook = "Stable"
        recommended_exposure = "Medium"
    else:
        sector_outlook = "Cautious"
        recommended_exposure = "Low"
    primary_sector = base_sectors[0] if base_sectors else "Diversified"
    primary_commodity = commodities[0] if commodities else "General"
    return {"primary_sectors": base_sectors, "primary_commodities": commodities, "recommended_sector": primary_sector, "recommended_commodity": primary_commodity, "sector_outlook": sector_outlook, "recommended_exposure": recommended_exposure}


def identify_opportunities(returns: Dict[str, float], momentum: Dict[str, float], volatility: Dict[str, float], risk_adjusted: Dict[str, float]) -> Dict[str, Any]:
    opportunities = []
    warnings = []
    if momentum['momentum_6m'] > 0.10 and risk_adjusted['sharpe_ratio'] > 0.5:
        opportunities.append("Strong risk-adjusted momentum indicates favorable entry conditions")
    if volatility['annualized_volatility'] < 0.20 and momentum['momentum_3m'] > 0:
        opportunities.append("Low volatility with positive momentum suggests stable growth environment")
    if risk_adjusted['sortino_ratio'] > 1.0:
        opportunities.append("Excellent downside protection relative to returns")
    if momentum['momentum_12m'] > 0.20:
        opportunities.append("Strong annual momentum indicates market confidence")
    if volatility['annualized_volatility'] > 0.35:
        warnings.append("High market volatility increases investment risk")
    if volatility['max_drawdown'] > 0.30:
        warnings.append("Significant drawdown history suggests periodic turbulence")
    if momentum['momentum_6m'] < -0.10:
        warnings.append("Negative momentum may indicate unfavorable near-term conditions")
    if risk_adjusted['sharpe_ratio'] < 0:
        warnings.append("Negative risk-adjusted returns suggest caution")
    if len(opportunities) >= 3:
        overall = "High Opportunity"
    elif len(opportunities) >= 1 and len(warnings) <= 1:
        overall = "Moderate Opportunity"
    elif len(warnings) >= 2:
        overall = "Proceed with Caution"
    else:
        overall = "Neutral"
    return {"opportunity_level": overall, "opportunities": opportunities, "warnings": warnings}


def plot_index_history(data: pd.DataFrame, country: str, index_name: str, period_label: str = "5 Year") -> None:
    if data is None or data.empty:
        print(f"No data available to plot for {country}")
        return
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{country} - {index_name} Market Analysis', fontsize=14, fontweight='bold')
    ax1 = axes[0, 0]
    ax1.plot(data.index, data['Close'], color='#2E86AB', linewidth=1.5)
    ax1.fill_between(data.index, data['Close'], alpha=0.3, color='#2E86AB')
    ax1.set_title(f'{period_label} Price History')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Index Value')
    ax1.grid(True, alpha=0.3)
    ax2 = axes[0, 1]
    if len(data) >= 50:
        sma_50 = data['Close'].rolling(50).mean()
        sma_200 = data['Close'].rolling(200).mean() if len(data) >= 200 else None
        ax2.plot(data.index, data['Close'], color='#2E86AB', linewidth=1, label='Price', alpha=0.7)
        ax2.plot(data.index, sma_50, color='#F18F01', linewidth=1.5, label='50 SMA')
        if sma_200 is not None:
            ax2.plot(data.index, sma_200, color='#C73E1D', linewidth=1.5, label='200 SMA')
        ax2.set_title('Moving Averages')
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)
    ax3 = axes[1, 0]
    daily_returns = data['Close'].pct_change().dropna()
    ax3.hist(daily_returns, bins=50, color='#2E86AB', alpha=0.7, edgecolor='black')
    ax3.axvline(daily_returns.mean(), color='#F18F01', linestyle='--', linewidth=2, label=f'Mean: {daily_returns.mean()*100:.2f}%')
    ax3.set_title('Daily Returns Distribution')
    ax3.set_xlabel('Daily Return')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax4 = axes[1, 1]
    rolling_max = data['Close'].expanding().max()
    drawdown = (data['Close'] - rolling_max) / rolling_max * 100
    ax4.fill_between(data.index, drawdown, 0, color='#C73E1D', alpha=0.5)
    ax4.set_title('Drawdown Analysis')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Drawdown (%)')
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_one_year_history(data: pd.DataFrame, country: str, index_name: str) -> None:
    if data is None or data.empty:
        print(f"No data available for 1-year plot for {country}")
        return
    one_year_ago = datetime.now() - timedelta(days=365)
    one_year_data = data[data.index >= one_year_ago]
    if one_year_data.empty:
        print(f"Insufficient 1-year data for {country}")
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(one_year_data.index, one_year_data['Close'], color='#2E86AB', linewidth=2)
    ax.fill_between(one_year_data.index, one_year_data['Close'], alpha=0.3, color='#2E86AB')
    start_val = one_year_data['Close'].iloc[0]
    end_val = one_year_data['Close'].iloc[-1]
    ytd_return = ((end_val / start_val) - 1) * 100
    ax.set_title(f'{country} - {index_name}\n1-Year Performance: {ytd_return:+.2f}%', fontsize=12, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Index Value')
    ax.grid(True, alpha=0.3)
    if len(one_year_data) >= 20:
        sma_20 = one_year_data['Close'].rolling(20).mean()
        ax.plot(one_year_data.index, sma_20, color='#F18F01', linewidth=1.5, linestyle='--', label='20 SMA')
        ax.legend()
    plt.tight_layout()
    plt.show()


def generate_country_report(country: str, country_info: Dict[str, Any], index_data: pd.DataFrame, currency_data: pd.DataFrame) -> Dict[str, Any]:
    returns = calculate_returns(index_data)
    volatility = calculate_volatility(index_data)
    momentum = calculate_momentum(index_data)
    risk_adjusted = calculate_risk_adjusted_returns(index_data)
    trend = calculate_trend_strength(index_data)
    currency_risk = calculate_currency_risk(currency_data)
    business_score = calculate_business_friendliness_score(country_info, index_data, currency_data)
    growth_probability = estimate_gdp_growth_probability(index_data, momentum, volatility)
    sectors = identify_growth_sectors(country_info, momentum)
    opportunities = identify_opportunities(returns, momentum, volatility, risk_adjusted)
    return {"country": country, "index": country_info.get('index', 'N/A'), "currency": country_info.get('currency', 'N/A'), "tax_rate": f"{country_info.get('tax_rate', 0) * 100:.1f}%", "business_friendliness": business_score, "market_metrics": {"total_return_5y": f"{returns['total_return'] * 100:.2f}%", "annualized_return": f"{returns['annualized_return'] * 100:.2f}%", "annualized_volatility": f"{volatility['annualized_volatility'] * 100:.2f}%", "max_drawdown": f"{volatility['max_drawdown'] * 100:.2f}%", "sharpe_ratio": round(risk_adjusted['sharpe_ratio'], 2), "sortino_ratio": round(risk_adjusted['sortino_ratio'], 2)}, "momentum": {"1_month": f"{momentum['momentum_1m'] * 100:.2f}%", "3_month": f"{momentum['momentum_3m'] * 100:.2f}%", "6_month": f"{momentum['momentum_6m'] * 100:.2f}%", "12_month": f"{momentum['momentum_12m'] * 100:.2f}%"}, "trend_analysis": {"trend_score": f"{trend['trend_score'] * 100:.1f}%", "above_50_sma": trend['above_sma_50'], "above_200_sma": trend['above_sma_200'], "golden_cross": trend['golden_cross']}, "currency_analysis": {"volatility": f"{currency_risk['currency_volatility'] * 100:.2f}%", "1y_trend": f"{currency_risk['currency_trend'] * 100:.2f}%", "risk_score": f"{currency_risk['currency_risk_score'] * 100:.1f}%"}, "growth_outlook": growth_probability, "sector_analysis": sectors, "opportunity_assessment": opportunities}


def print_report(report: Dict[str, Any]) -> None:
    print("\n" + "="*80)
    print(f"COUNTRY INVESTMENT ANALYSIS: {report['country'].upper()}")
    print("="*80)
    print(f"\nIndex: {report['index']}")
    print(f"Currency: {report['currency']}")
    print(f"Corporate Tax Rate: {report['tax_rate']}")
    print("\n" + "-"*40)
    print("BUSINESS FRIENDLINESS SCORE")
    print("-"*40)
    bf = report['business_friendliness']
    print(f"  Overall Score: {bf['overall_score']}/100")
    print(f"  - Base Ease of Business: {bf['base_ease_of_business']}%")
    print(f"  - Tax Efficiency: {bf['tax_efficiency_score']}%")
    print(f"  - Market Liquidity: {bf['market_liquidity_score']}%")
    print(f"  - Market Stability: {bf['market_stability_score']}%")
    print(f"  - Currency Stability: {bf['currency_stability_score']}%")
    print(f"  - Growth Potential: {bf['growth_potential_score']}%")
    print("\n" + "-"*40)
    print("MARKET PERFORMANCE METRICS")
    print("-"*40)
    mm = report['market_metrics']
    print(f"  5-Year Total Return: {mm['total_return_5y']}")
    print(f"  Annualized Return: {mm['annualized_return']}")
    print(f"  Annualized Volatility: {mm['annualized_volatility']}")
    print(f"  Maximum Drawdown: {mm['max_drawdown']}")
    print(f"  Sharpe Ratio: {mm['sharpe_ratio']}")
    print(f"  Sortino Ratio: {mm['sortino_ratio']}")
    print("\n" + "-"*40)
    print("MOMENTUM INDICATORS")
    print("-"*40)
    mom = report['momentum']
    print(f"  1-Month: {mom['1_month']}")
    print(f"  3-Month: {mom['3_month']}")
    print(f"  6-Month: {mom['6_month']}")
    print(f"  12-Month: {mom['12_month']}")
    print("\n" + "-"*40)
    print("TREND ANALYSIS")
    print("-"*40)
    ta = report['trend_analysis']
    print(f"  Trend Score: {ta['trend_score']}")
    print(f"  Above 50 SMA: {'Yes' if ta['above_50_sma'] else 'No'}")
    print(f"  Above 200 SMA: {'Yes' if ta['above_200_sma'] else 'No'}")
    print(f"  Golden Cross: {'Yes' if ta['golden_cross'] else 'No'}")
    print("\n" + "-"*40)
    print("CURRENCY ANALYSIS")
    print("-"*40)
    ca = report['currency_analysis']
    print(f"  Currency Volatility: {ca['volatility']}")
    print(f"  1-Year Trend vs USD: {ca['1y_trend']}")
    print(f"  Currency Risk Score: {ca['risk_score']}")
    print("\n" + "-"*40)
    print("GROWTH OUTLOOK")
    print("-"*40)
    go = report['growth_outlook']
    print(f"  GDP Growth Probability: {go['gdp_growth_probability']}%")
    print(f"  Investment Growth Probability: {go['investment_growth_probability']}%")
    print("\n" + "-"*40)
    print("SECTOR ANALYSIS")
    print("-"*40)
    sa = report['sector_analysis']
    print(f"  Primary Sectors: {', '.join(sa['primary_sectors'])}")
    print(f"  Key Commodities: {', '.join(sa['primary_commodities'])}")
    print(f"  Recommended Sector: {sa['recommended_sector']}")
    print(f"  Recommended Commodity: {sa['recommended_commodity']}")
    print(f"  Sector Outlook: {sa['sector_outlook']}")
    print(f"  Recommended Exposure: {sa['recommended_exposure']}")
    print("\n" + "-"*40)
    print("OPPORTUNITY ASSESSMENT")
    print("-"*40)
    oa = report['opportunity_assessment']
    print(f"  Opportunity Level: {oa['opportunity_level']}")
    if oa['opportunities']:
        print("  Opportunities:")
        for opp in oa['opportunities']:
            print(f"    + {opp}")
    if oa['warnings']:
        print("  Warnings:")
        for warn in oa['warnings']:
            print(f"    ! {warn}")
    print("\n" + "="*80)


def analyze_country(country: str, show_charts: bool = True, show_1y_chart: bool = True) -> Optional[Dict[str, Any]]:
    country_mapping = get_country_index_mapping()
    country_key = None
    for key in country_mapping.keys():
        if key.lower() == country.lower():
            country_key = key
            break
    if country_key is None:
        print(f"Country '{country}' not found in database.")
        print(f"Available countries: {', '.join(sorted(country_mapping.keys()))}")
        return None
    country_info = country_mapping[country_key]
    print(f"\nFetching data for {country_key}...")
    index_data = fetch_index_data(country_info['index'], period="5y")
    if index_data is None:
        print(f"Could not fetch index data for {country_key}")
        return None
    currency_data = None
    if country_info.get('currency_pair'):
        currency_data = fetch_currency_data(country_info['currency_pair'], period="1y")
    report = generate_country_report(country_key, country_info, index_data, currency_data)
    print_report(report)
    if show_charts:
        plot_index_history(index_data, country_key, country_info['index'], "5 Year")
    if show_1y_chart:
        plot_one_year_history(index_data, country_key, country_info['index'])
    return report


def analyze_all_countries(show_charts: bool = False) -> List[Dict[str, Any]]:
    country_mapping = get_country_index_mapping()
    all_reports = []
    for country in country_mapping.keys():
        print(f"\n{'='*60}")
        print(f"Analyzing {country}...")
        print('='*60)
        report = analyze_country(country, show_charts=show_charts, show_1y_chart=False)
        if report:
            all_reports.append(report)
    return all_reports


def compare_countries(countries: List[str]) -> pd.DataFrame:
    reports = []
    for country in countries:
        report = analyze_country(country, show_charts=False, show_1y_chart=False)
        if report:
            reports.append(report)
    if not reports:
        print("No valid country data retrieved.")
        return pd.DataFrame()
    comparison_data = []
    for r in reports:
        comparison_data.append({"Country": r['country'], "Business Score": r['business_friendliness']['overall_score'], "Annualized Return": r['market_metrics']['annualized_return'], "Volatility": r['market_metrics']['annualized_volatility'], "Sharpe Ratio": r['market_metrics']['sharpe_ratio'], "GDP Growth Prob": r['growth_outlook']['gdp_growth_probability'], "Investment Prob": r['growth_outlook']['investment_growth_probability'], "Opportunity Level": r['opportunity_assessment']['opportunity_level'], "Recommended Sector": r['sector_analysis']['recommended_sector']})
    df = pd.DataFrame(comparison_data)
    df = df.sort_values('Business Score', ascending=False)
    print("\n" + "="*100)
    print("COUNTRY COMPARISON")
    print("="*100)
    print(df.to_string(index=False))
    return df


def rank_all_countries() -> pd.DataFrame:
    country_mapping = get_country_index_mapping()
    all_countries = list(country_mapping.keys())
    return compare_countries(all_countries)


def run_country_analysis(country: str = None, analyze_all: bool = False, compare: List[str] = None, show_charts: bool = True, show_1y_chart: bool = True) -> Any:
    if analyze_all:
        return analyze_all_countries(show_charts=False)
    elif compare:
        return compare_countries(compare)
    elif country:
        return analyze_country(country, show_charts=show_charts, show_1y_chart=show_1y_chart)
    else:
        print("Please specify a country, set analyze_all=True, or provide a list of countries to compare.")
        return None


if __name__ == "__main__":
    run_country_analysis("United States")
