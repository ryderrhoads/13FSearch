"""
Name: 13f_search.py
Author: Ryder Rhoads
Company: Wedbush Secruities
Summary: The goal of this program is to find all institutional clients which hold the given tickers. With the goal of creating business at the firm.
Requires: https://pandas.pydata.org/ & https://sec-api.io/ 
"""
from sec_api import QueryApi
import pandas as pd
from datetime import datetime, timedelta


def main():
    """
    Main purpose of th
    """
    queryApi = QueryApi(api_key="your_key_here")
    sheet = []  # Create an empty list to store data from each iteration
    
    latest_date = datetime.strptime("2023-02-27", "%Y-%m-%d")
    current_date = datetime.strptime("2023-05-28", "%Y-%m-%d") 
    date = datetime.strptime("2023-02-28", "%Y-%m-%d")  
    formatted_latest_date = latest_date.strftime("%Y-%m-%d")
    formatted_current_date = current_date.strftime("%Y-%m-%d")
    formatted_date = date.strftime("%Y-%m-%d")

    while date <= current_date:
        formatted_latest_date = latest_date.strftime("%Y-%m-%d")
        formatted_current_date = current_date.strftime("%Y-%m-%d")
        formatted_date = date.strftime("%Y-%m-%d")
        for tikr in BIOTECH_COMPANIES:
            query = {
                "query": {
                    "query_string": {
                        "query": f"formType:\"13F\" AND holdings.ticker:{tikr} AND filedAt:[{formatted_latest_date} TO {formatted_date}]"
                    }
                },
                "from": "0",
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            print(f"Query pulled FROM {formatted_latest_date} TO {formatted_date} FOR {tikr}")
            filings = queryApi.get_filings(query)  # Retrieve filings for the current ticker
            filings_data = get_filings(filings)  # Process filings data into a list
            sheet.extend(filings_data)  # Append the filings data to the 'sheet' list
        
        latest_date += timedelta(days=1)  # Increment the date by 1 day
        date += timedelta(days=1)  # Increment the date by 1 day
    
    # Convert 'sheet' list into a pandas DataFrame
    df = pd.DataFrame(sheet, columns=["Company Name", "Total Value", "Position Value", "Position Percentage"])

    # Save the DataFrame as an Excel file 
    df.to_excel("13FSearch/output.xlsx", index=False)


def get_filings(filings):
    i = 0
    sheet=[]
    for f in filings.items():
        if i == 2:
            if len(f[1]) ==200:
                print("OVER LIMIT QUERIES")
                print(f[1])
            for i in f[1]:
                tot = 0
                positionVal = 0
                info = [i['companyName']]
                for holding in i["holdings"]:
                    tot += holding["value"]
                    try:
                        if holding["ticker"] in BIOTECH_COMPANIES and holding["shrsOrPrnAmt"]['sshPrnamtType'] == "SH":
                            positionVal += holding["value"]
                    except KeyError:
                        continue
                info.append(tot)
                info.append(positionVal)
                info.append(float(positionVal / tot))
                sheet.append(info)
            break
        i+=1
    return sheet

main()
