import requests
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
load_dotenv()
import datetime as dt
import zoneinfo

scope = ["https://www.googleapis.com/auth/spreadsheets"]
credns = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(credns)
#google workbook id load from .env file
sheet_id = os.getenv("SHEET_ID")
#open workbook 
workbook = client.open_by_key(sheet_id)


base_url="https://www.cse.lk/api/"
end_point="companyInfoSummery"
banks = ["COMB.N0000","SEYB.N0000","SAMP.N0000","HNB.N0000","DIPD.N0000","TJL.N0000","AHUN.N0000","SERV.N0000"]
bank_names = ["Commercial","Seylan","Sampath","HNB","Dipped Product","TeeJay","Aitken","Kingsbury"]
last_trade_price=[]
price_to_book_value=[]

def get_colombo_time_zoneinfo():
    """Gets the current time in Colombo using zoneinfo."""
    try:
        # Define the time zone object for Colombo
        tz_colombo = zoneinfo.ZoneInfo("Asia/Colombo")
        
        # Get the current time with the specified timezone
        current_time_colombo = dt.datetime.now(tz=tz_colombo)
        
        # Format the time for display
        formatted_time = current_time_colombo.strftime("%Y-%m-%d %H:%M:%S %Z")
        return formatted_time

    except zoneinfo.ZoneInfoNotFoundError:
        return "Timezone 'Asia/Colombo' not found. Ensure the tzdata package is installed."
    except Exception as e:
        return f"An error occurred: {e}"

# fetch latest data from CSE website
for bank in banks:
    data = {"symbol": bank}
    response = requests.post(base_url + end_point, data=data)
    #print(f"Status code: {response.status_code}")
    infor= response.json()
    infor_2 = infor['reqSymbolInfo']
    # update last trade price in a list
    last_trade_price.append(infor_2["lastTradedPrice"])


#open the "watchlist" sheet
sheet = workbook.worksheet('watchlist')
#update cells
sheet.update_cell(2,6,last_trade_price[0])
sheet.update_cell(3,6,last_trade_price[1])
sheet.update_cell(4,6,last_trade_price[2])
sheet.update_cell(5,6,last_trade_price[3])
sheet.update_cell(6,6,last_trade_price[4])
sheet.update_cell(7,6,last_trade_price[5])
sheet.update_cell(8,6,last_trade_price[6])
sheet.update_cell(9,6,last_trade_price[7])

# retrieve price to book value from google sheet
for row in range (2,9,1):
    price_to_book_value.append(sheet.cell(row,9).value)
#print message if any company reaches PBV less than 0.81
for i in range (0,7,1):
    if float(price_to_book_value[i]) < 0.81 :
        print(f"Buying target reach {bank_names[i]} @ {last_trade_price[i]}")

# get current tile
colombo_time = get_colombo_time_zoneinfo()
#print(f"Current time in Colombo: {colombo_time}")
#update last update date time in the sheet
sheet.update_cell(15,2,colombo_time)



