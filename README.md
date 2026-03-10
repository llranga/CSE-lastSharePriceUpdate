This code checks last share price of predefined companies in Colombo Stock Exchange (CSE) on weekdays every hour between 09:00 to 15:00. last share price is updated in google sheet. price to book value is calculated in the google sheet. when price to book value reaches a predefined ratio, code send a telegram message with company name and latest share price.
Code is scheduled to run on time zone Asia/Colombo
credentials.json contains google sheet API
.env must be created with google sheet id, telegram bot api and chat id
a root level logs folder must be created 
