#!/usr/bin/env python
import json
import re
import json
import requests

class Yahoo_data_class:
    def __init__(self, name):
        self.name = name 

    def get_fundamental_data(self, thicker):
        self.thicker = thicker
        url = 'https://finance.yahoo.com/quote/'+thicker+'/key-statistics'
        try:
            html_text = requests.get(url).text
            data = json.loads(re.search(r'root\.App\.main = (.*?\});\n', html_text).group(1))

            # uncomment this to print all data:
            # print(json.dumps(data, indent=4))
            data_list = {}
            data_list['shortName']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['quoteType']['shortName']
            data_list['mcap']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['marketCap']['fmt']
            data_list['float']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['floatShares']['fmt']
            data_list['avg_volume']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['averageDailyVolume3Month']['fmt']

            data_list['insider_own']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['heldPercentInsiders']['fmt']
            data_list['institution_own']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['heldPercentInstitutions']['fmt']
            data_list['short_ratio']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['shortRatio']['fmt']
            data_list['pm_price']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['postMarketPrice']['fmt']
            data_list['prev_close_price']=data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPreviousClose']['fmt']
            
            data_list['gap']=str(round((1-(float(data_list['prev_close_price'])/float(data_list['pm_price'])))*100, 1))
            return data_list
        except KeyError:
            print(f"Thicker symbol '{thicker}' not found.")
            pass
    
