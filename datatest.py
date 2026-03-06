import api
import trademath
from typing import List, Dict
#from datetime import datetime

TAG_IDS = {
	"politics": "2",
	"geopolitics": "100265"

}

TOPICS_WE_LIKE = ["greenland", "venezuela", "iran", "israel" ]      #check for spelling errors lol, always lowercase

GammaTest = api.Gamma_API() 										# start gamma session, create gamma object for access to methods

markets = GammaTest.get_markets(TAG_IDS["geopolitics"], limit=100)  # pull markets from api using gamma object

Data = api.Data_API()

all_trades = []

for conditionId in markets:
	all_trades.append(Data.get_trades(market=conditionId))

print(all_trades)


