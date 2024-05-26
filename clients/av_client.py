import json
import requests
import sys
import os
from tqdm import tqdm
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import ALPHA_VANTAGE_API_KEY
from src.styles import GREEN, RED, RESET

API_KEY = ALPHA_VANTAGE_API_KEY

def saveToFile(data, outputPath):
    with open(outputPath, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def fetchData(url):
    response = requests.get(url)
    try:
        data = response.json()
        return data
    except requests.exceptions.JSONDecodeError as e:
        tqdm.write(f"{RED}Failed to decode JSON for URL: {url}{RESET}")
        tqdm.write(f"{RED}Error: {e}{RESET}")
        return None

def filterByDate(reports, years=2):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    return [
        report for report in reports
        if datetime.strptime(report['fiscalDateEnding'], '%Y-%m-%d') >= start_date
    ]

def filterTechnicalData(data, years=2):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    filtered_data = {
        date: values for date, values in data.items()
        if datetime.strptime(date, '%Y-%m-%d') >= start_date
    }
    return filtered_data

def getCompanyOverview(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    saveToFile(data, outputPath)
    return data

def getIncomeStatement(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    if data:
        if 'annualReports' in data:
            data['annualReports'] = filterByDate(data['annualReports'])
        if 'quarterlyReports' in data:
            data['quarterlyReports'] = filterByDate(data['quarterlyReports'])
    saveToFile(data, outputPath)
    return data

def getBalanceSheet(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    if data:
        if 'annualReports' in data:
            data['annualReports'] = filterByDate(data['annualReports'])
        if 'quarterlyReports' in data:
            data['quarterlyReports'] = filterByDate(data['quarterlyReports'])    
    saveToFile(data, outputPath)
    return data

def getCashFlow(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    if data:
        if 'annualReports' in data:
            data['annualReports'] = filterByDate(data['annualReports'])
        if 'quarterlyReports' in data:
            data['quarterlyReports'] = filterByDate(data['quarterlyReports'])
    saveToFile(data, outputPath)
    return data

def getEarnings(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    if data:
        if 'annualEarnings' in data:
            data['annualEarnings'] = filterByDate(data['annualEarnings'])
        if 'quarterlyEarnings' in data:
            data['quarterlyEarnings'] = filterByDate(data['quarterlyEarnings'])
    saveToFile(data, outputPath)
    return data

def getGlobalQuote(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    saveToFile(data, outputPath)
    return data

def getTimeSeriesDaily(ticker, outputPath):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}'
    data = fetchData(url)
    saveToFile(data, outputPath)
    return data

def getTechnicalIndicators(ticker, outputPath):
    baseURL = 'https://www.alphavantage.co/query?'
    indicators = {
        'SMA': f'{baseURL}function=SMA&symbol={ticker}&interval=daily&time_period=20&series_type=close&apikey={API_KEY}',
        'EMA': f'{baseURL}function=EMA&symbol={ticker}&interval=daily&time_period=20&series_type=close&apikey={API_KEY}',
        'RSI': f'{baseURL}function=RSI&symbol={ticker}&interval=daily&time_period=14&series_type=close&apikey={API_KEY}',
        'STOCH': f'{baseURL}function=STOCH&symbol={ticker}&interval=daily&apikey={API_KEY}',
        'BBANDS': f'{baseURL}function=BBANDS&symbol={ticker}&interval=daily&time_period=20&series_type=close&apikey={API_KEY}',
        'VOLUME': f'{baseURL}function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={API_KEY}'
    }
    
    results = {}
    for indicator, url in indicators.items():
        tqdm.write(f"{GREEN}Retrieving {indicator}{RESET}")
        data = fetchData(url)
        if data and f'Technical Analysis: {indicator}' in data:
            technicalData = data[f'Technical Analysis: {indicator}']
            data[f'Technical Analysis: {indicator}'] = filterTechnicalData(technicalData)
            results[indicator] = data
    
    saveToFile(results, outputPath)
    return results

def getFundamentals(ticker):
    basePath = f'datasets/fundamentals/{ticker}'
    os.makedirs(basePath, exist_ok=True)  #Ensure it exists

    tasks = [
        (f"{GREEN}Retrieving company overview{RESET}", getCompanyOverview, ticker, f'{basePath}/{ticker}_companyOverview.json'),
        (f"{GREEN}Retrieving income statement{RESET}", getIncomeStatement, ticker, f'{basePath}/{ticker}_incomeStatement.json'),
        (f"{GREEN}Retrieving balance sheet{RESET}", getBalanceSheet, ticker, f'{basePath}/{ticker}_balanceSheet.json'),
        (f"{GREEN}Retrieving cash flow{RESET}", getCashFlow, ticker, f'{basePath}/{ticker}_cashFlow.json'),
        (f"{GREEN}Retrieving earnings{RESET}", getEarnings, ticker, f'{basePath}/{ticker}_earnings.json'),
        (f"{GREEN}Retrieving global quote{RESET}", getGlobalQuote, ticker, f'{basePath}/{ticker}_globalQuote.json'),
        (f"{GREEN}Retrieving time series daily{RESET}", getTimeSeriesDaily, ticker, f'{basePath}/{ticker}_timeSeriesDaily.json'),
        (f"{GREEN}Retrieving technical indicators{RESET}", getTechnicalIndicators, ticker, f'{basePath}/{ticker}_technicalIndicators.json')
    ]

    for description, func, arg, outputPath in tqdm(tasks, desc="Overall Progress", unit="task"):
        tqdm.write(description)
        os.makedirs(os.path.dirname(outputPath), exist_ok=True)
        func(arg, outputPath)
