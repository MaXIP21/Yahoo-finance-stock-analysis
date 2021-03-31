#!/usr/bin/env python
import json
import re
import json
import requests

class Yahoo_data_class:
    def __init__(self, name):
        self.name = name 

    def get_tree_data(self, keylist):
        #print(len(keylist))
        try:
            if len(keylist) == 2:
                select_data=self.data['context']['dispatcher']['stores'][keylist[0]][keylist[1]]
            if len(keylist) == 3:
                select_data=self.data['context']['dispatcher']['stores'][keylist[0]][keylist[1]][keylist[2]]
            if len(keylist) == 4:
                select_data=self.data['context']['dispatcher']['stores'][keylist[0]][keylist[1]][keylist[2]][keylist[3]]
        except Exception as e:
            #print("Error : "+str(e))
            select_data = "N/A"
        return select_data

    def get_fundamental_data(self, thicker):
        self.thicker = thicker
        url = 'https://finance.yahoo.com/quote/'+thicker+'/key-statistics'
        try:
            html_text = requests.get(url).text
            self.data = json.loads(re.search(r'root\.App\.main = (.*?\});\n', html_text).group(1))

            # uncomment this to print all data:
            # print(json.dumps(data, indent=4))
            self.data_list = {}

            self.data_list['shortName']=self.get_tree_data(['QuoteSummaryStore','quoteType', 'shortName'])
            self.data_list['mcap']=self.get_tree_data(['QuoteSummaryStore','price', 'marketCap','fmt'])
            self.data_list['float']=self.get_tree_data(['QuoteSummaryStore','defaultKeyStatistics', 'floatShares','fmt'])
            self.data_list['avg_volume']=self.get_tree_data(['QuoteSummaryStore','price', 'averageDailyVolume3Month','fmt'])
            self.data_list['insider_own']=self.get_tree_data(['QuoteSummaryStore','defaultKeyStatistics', 'heldPercentInsiders','fmt'])
            self.data_list['institution_own']=self.get_tree_data(['QuoteSummaryStore','defaultKeyStatistics', 'heldPercentInstitutions','fmt'])
            self.data_list['short_ratio']=self.get_tree_data(['QuoteSummaryStore','defaultKeyStatistics', 'shortRatio','fmt'])
            self.data_list['pm_price']=self.get_tree_data(['QuoteSummaryStore','price', 'postMarketPrice','fmt'])
            self.data_list['prem_price']=self.get_tree_data(['QuoteSummaryStore','price', 'preMarketPrice','fmt'])
            self.data_list['prev_close_price']=self.get_tree_data(['QuoteSummaryStore','financialData', 'currentPrice','fmt'])

            close_price=float(self.data_list['prev_close_price'])
            prem_price=float(self.data_list['prem_price'])
            if close_price>0 and prem_price>0 :
                self.data_list['gap']=str(round(float(((prem_price/close_price)-1)*100), 2))
            else:
                self.data_list['gap']="N/A"
            #return data_list
        except KeyError:
            print(f"Thicker symbol '{thicker}' not found.")
            pass
    
