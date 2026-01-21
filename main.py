import api
from typing import List, Dict
#from datetime import datetime

TAG_IDS = {
	"politics": "2",
	"geopolitics": "100265"

}

TOPICS_WE_LIKE = ["greenland", "venezuela", "iran", "israel" ] #dont forget caps management #check for spelling errors lol


GammaTest = api.Gamma_API() 										# start gamma session, create gamma object for access to methods

markets = GammaTest.get_markets(TAG_IDS["geopolitics"], limit=100)  # pull markets from api using gamma object

#print(markets[1])													# print markets for testing

conditionIdList = api.market_filter(markets, TOPICS_WE_LIKE)		# filter for keywords and return list of conditionIds to be used with clob, prints each approved market

GammaTest.end_session()												# kill gamma session


#print(conditionIdList)												# print conditionIdList for testing

ClobTest = api.Clob_API()											# start Clob session, create clob object for access to methods

tempEventData = ClobTest.event_data(conditionIdList[-1])		    # generate temporary event data to test token function in api, -1 is lowest in word search print

tokenTest = ClobTest.tokens(eventData=tempEventData)				# using event data, pull token_id value, returns LIST OF DICTS, tokens value contains both yes and no

#print(f"{tokenTest}\n")											# print token_id result for testing

#orderBookTest = ClobTest.client.get_order_book(tokenTest[0]["token_id"]) # calls client.get_order_book using "yes" tokens token_id

#print(f"{ClobTest.retrieve_bids(OrderBookSummary=orderBookTest)}")      # prints list of dicts of bids generated with retrieve_bids method for Clob_API

DataTest = api.Data_API()

getTradesTest = DataTest.get_trades(market=[conditionIdList[-1]], takerOnly=True)

print(getTradesTest)

# 
# So far then, we have used the gamma api to find suitable markets, used the resulting conditionIds to access and store bids from clob. The issue is, there is no account  
# data associated with the bids...  I dont think we're looking for bids actually
#



#print(ClobTest.client.get_order_books([BookParams(token_id=tokenTest[0]["token_id"])])) 
'''
solved issue: condition id held within event, resolved markets_culled to now hold condition IDs
issues:
	muthafuckin uhh BookParams not recognized despite import. Why? 
	client.get_order_book returns objects, read documentation
'''