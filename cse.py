import requests
import time

base_url="https://www.cse.lk/api/"
end_point="companyInfoSummery"

class CSE:
    def __init__(self, companies:list, company_names:list):
        self.companies=companies
        self.company_names = company_names
        

    def get_last_trade_price(self):
        last_trade_price=[]
        for company in self.companies:
            data = {"symbol": company}
            response = requests.post(base_url + end_point, data=data)
            #print(f"Status code: {response.status_code}")
            infor= response.json()
            infor_2 = infor['reqSymbolInfo']
            # update last trade price in a list
            last_trade_price.append(infor_2["lastTradedPrice"])
            time.sleep(2)
            
        return last_trade_price