import api
import trademath
from typing import List, Dict
#from datetime import datetime

TAG_IDS = {
	"politics": "2",
	"geopolitics": "100265"

}

TOPICS_WE_LIKE = ["greenland", "venezuela", "iran", "israel" ] #dont forget caps management #check for spelling errors lol

GammaTest = api.Gamma_API() 										# start gamma session, create gamma object for access to methods

markets = GammaTest.get_markets(TAG_IDS["geopolitics"], limit=100)  # pull markets from api using gamma object

print(markets[1])													# print markets for testing

conditionIdList = api.market_filter(markets, TOPICS_WE_LIKE)		# filter for keywords and return list of conditionIds to be used with clob, prints each approved market

GammaTest.end_session()												# kill gamma session


print(conditionIdList)												# print conditionIdList for testing

#ClobTest = api.Clob_API()											# start Clob session, create clob object for access to methods

#tempEventData = ClobTest.event_data(conditionIdList[-1])		    # generate temporary event data to test token function in api, -1 is lowest in word search print

#tokenTest = ClobTest.tokens(eventData=tempEventData)				# using event data, pull token_id value, returns LIST OF DICTS, tokens value contains both yes and no

#print(f"{tokenTest}\n")											# print token_id result for testing

#orderBookTest = ClobTest.client.get_order_book(tokenTest[0]["token_id"]) # calls client.get_order_book using "yes" tokens token_id

#print(f"{ClobTest.retrieve_bids(OrderBookSummary=orderBookTest)}")      # prints list of dicts of bids generated with retrieve_bids method for Clob_API

DataTest = api.Data_API()

### note for get_trades: market parameter must be list conditionId strings ###

#getTradesTest = [] # List of list of dicts each list of dicts is a market 
#for conditionId in conditionIdList:
#	getTradesTest.append(DataTest.gt_trades(market=[conditionId], takerOnly=True, limit=1000))

getTradesTest = DataTest.get_trades(market=conditionIdList)









'''

 So far then, we have used the gamma api to find suitable markets, used resulting conditionIds to poll DataApi to retrieve 
 trades and asociated transactionHash / wallets/ asset/ timestamp. Goal now is to do math to find
 outliers and confidence in insider trading. Would like to do this without unnessicary rerunning
 which means saving information as we go. When we find outliers, and view their other trades for confidence, we need
 to poll all our other outlier lists for their user without running searches for outliers again. 


'''

