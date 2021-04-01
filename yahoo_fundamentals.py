#!/usr/bin/env python

import argparse
import os
import logging
import yahoo_data as yd
import finviz_class as fv
import pandas as pd

pd.set_option('display.max_colwidth', None)

def get_args():
    parser = argparse.ArgumentParser(prog='yahoo_fundamentals.py', 
                                    description="Yahoo Fundamental scraper, getting fundamental data from thickers",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--logfile', type=str, dest='logfile', 
                        default="yahoo_scraper",
                        help='Log is saved to this file.')
    
    parser.add_argument('-s','--stock', metavar='stock', type=str, 
                        help='Thicker of the stock.')

    parser.add_argument('-n','--news', dest='news', action='store_true', 
                        help='Fetch news.')
    
    parser.add_argument('--LOG', type=str, metavar='LOG_LEVEL', dest='LOG',
                        choices=['DEBUG', 'WARNING', 'ERROR', 'CRITICAL', 'INFO'],
                        default=os.environ.get('LOG', default='INFO').upper(),
                        help='Set the log level using environment variable LOG.')
    
    return parser.parse_args()


def main():
    args = get_args()
    
    log_level = getattr(logging, args.LOG, None)
    if not isinstance(log_level, int):
        raise ValueError('Invalid log level: %s' % args.LOG)
    logging.basicConfig(filemode='w', filename=args.logfile + '.log', level=log_level)
    logging.info("Initializing ScraperClass")
    yahoo=yd.Yahoo_data_class('Yahoo Scraper')
    finviz=fv.Finviz_data_class(args.stock)
    finviz.grab_data()
    finviz.get_fundamentals()
    
    if args.stock is not None:
        yahoo.get_fundamental_data(args.stock)
        yahoo_dict=yahoo.data_list
    else:
        print("Stock Thicker not defined please use -h to display help!")
        exit(1)

    if yahoo_dict != None:
        logging.info(yahoo_dict)
        #print(yahoo_dict)
        print("Stock : "+yahoo.thicker.upper())
        print("Company name  : "+yahoo_dict["shortName"])
        print("Labels : ")
        if (yahoo_dict["mcap_raw"] != "N/A" and float(yahoo_dict["mcap_raw"]) < 380000000):
            print("\t[ Small Cap ] ")
        if (yahoo_dict["float_raw"] != "N/A" and float(yahoo_dict["float_raw"]) < 10000000):
            print("\t[ Low Float ] ")
        print("---------------------------------------")
        print("\tMarketCap                 : "+yahoo_dict["mcap"])
        if (yahoo_dict["float"] != "N/A"):
            print("\tFloat                     : "+yahoo_dict["float"])
        else:
            print("\tFloat                     : "+finviz.get_dataframe_row("Shs Float"))
        print("\tAverage Volume            : "+yahoo_dict["avg_volume"])
        print("\tInsider Ownership         : "+yahoo_dict["insider_own"])
        print("\tInstitutional Ownership   : "+yahoo_dict["institution_own"])
        print("\tShort ratio               : "+yahoo_dict["short_ratio"]+"%")
        print("---------------------------------------")
        print("\tPost-market price : "+str(yahoo_dict["pm_price"]))
        print("\tPrev close price  : "+str(yahoo_dict["prev_close_price"]))
        print("\tPre-market price  : "+str(yahoo_dict["prem_price"]))
        yahoo.calculate_gap()
        if(yahoo_dict["gap"] != "N/A"):
            print("\tGAP               : "+str(yahoo_dict["gap"])+"%")
        else:
            print("\tGAP               : "+str(finviz.get_dataframe_row("Change")))
    if args.news is not None:
        finviz.get_news()
        print("\nHeadlines : \n")
        for ad in range(1,4):
            print("  "+finviz.news.values[ad][0])
            print("\t\t"+finviz.news.values[ad][1])
            print("\t\t"+finviz.news.values[ad][2])

        #for news_index in range(0,3):
        #    date=finviz.news.index[news_index]
            
        #    print(finviz.news['News Headline'][0])
    
    #print(finviz.get_dataframe_row("Shs Float"))
    #print(finviz.get_news())

if __name__ == "__main__":
    main()
    logging.info("CLI activated")




