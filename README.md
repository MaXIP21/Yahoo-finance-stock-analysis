# Yahoo Stock Analysis Python

This script is created to gather stock fundamental data from yahoo finance. 

## Help
usage: yahoo_fundamentals.py [-h] [--logfile LOGFILE] [-s stock]
                             [--LOG LOG_LEVEL]

Yahoo Fundamental scraper, getting fundamental data from thickers

optional arguments:\n
  -h, --help            show this help message and exit\n
  --logfile LOGFILE     Log is saved to this file. (default: yahoo_scraper)\n
  -s stock, --stock stock\n
                        Thicker of the stock. (default: None)\n
  --LOG LOG_LEVEL       Set the log level using environment variable LOG.\n
                        (default: INFO)\n
