from pytz import timezone
import gspread
import time
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import logging
from localtime import Localtime
from cse import CSE
from telegrammessage import TelegramMessage 
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()
# open existing google sheet workbook
scope = ["https://www.googleapis.com/auth/spreadsheets"]
credns = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(credns)
#google sheet id load from .env file
sheet_id = os.getenv("SHEET_ID")

#telegram chat_id and bot_token
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

#open workbook 
workbook = client.open_by_key(sheet_id)
#define variables
banks = ["COMB.N0000","SEYB.N0000","SAMP.N0000","HNB.N0000","DIPD.N0000","TJL.N0000","AHUN.N0000","SERV.N0000"]
bank_names = ["Commercial","Seylan","Sampath","HNB","Dipped Product","TeeJay","Aitken","Kingsbury"]

# logging logs folder
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
                        )

def update():
    last_trade_price=[]
    price_to_book_value=[]

    # create  my cse with known company code and names
    my_cse = CSE(banks,bank_names)
    last_trade_price = my_cse.get_last_trade_price()

    #create telegram message instance
    my_chat = TelegramMessage(bot_token,chat_id)

    #open the "watchlist" sheet of google sheet workbook
    sheet = workbook.worksheet('watchlist')
    #update cells
    for i in range (0,7,1):
        sheet.update_cell(i+2,6,last_trade_price[i])
    #wait for 1 second 
    time.sleep(1)
    # retrieve price to book value from google sheet
    for row in range (2,9,1):
        price_to_book_value.append(sheet.cell(row,9).value)
    #print message if any company reaches PBV less than 0.81
    for i in range (0,7,1):
        if float(price_to_book_value[i]) < 0.9 :
            #print(f"Buying target reach {bank_names[i]} @ {last_trade_price[i]}")
            # send telegram message
            my_chat.send_message(f"Buying target reach {bank_names[i]} @ {last_trade_price[i]}")
            logging.info(f"Buying target reach {bank_names[i]} @ {last_trade_price[i]}")
            time.sleep(0.5)
    
    # get current time
    colombo_time = Localtime("Asia/Colombo").get_local_time()
    #update last update date time in the sheet
    sheet.update_cell(15,2,colombo_time)
    #log google sheet time updated
    logging.info("Last update time updated in google sheet")

def main():
    # schedule time is base on Asia/Colombo time
    #log program started
    logging.info("main function started")
    scheduler = BlockingScheduler(timezone = timezone("Asia/Colombo"))
    scheduler.add_job (update,
                      'cron',
                      day_of_week='mon-fri',
                      hour='20-23',
                      minute=0 
                      )
    scheduler.start()


if __name__ == "__main__":
    main()






