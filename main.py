import api
import trademath
import json
import time
from typing import List, Dict


TAG_IDS = {
	"politics": "2",
	"geopolitics": "100265"

}

TOPICS_WE_LIKE = ["greenland", "venezuela", "iran", "israel", ]      #check for spelling errors, always lowercase

GammaTest = api.Gamma_API() 										 #start gamma session

print("Fetching markets..... (rate limited)")

markets = GammaTest.get_markets_by_pagination(tag_id=TAG_IDS["geopolitics"], offset=3, limit=50) 	 # query markets from api using gamma object
print(f"Total markets: {len(markets)}")

event_data_list = GammaTest.get_event_data(markets=markets)										 	 #Prep for time analysis later

print(f"Active events: {len(event_data_list)}")

conditionIdList = [event["conditionId"] for event in event_data_list]								 #Get conditionId list, should be method 


#conditionIdList = api.market_filter(markets, TOPICS_WE_LIKE)		# filter for keywords and return list of conditionIds to be used with clob, prints each approved market
len_before_culling = len(conditionIdList)
#print(f"# MARKETS AFTER FILTER: {len_before_culling}")
#print(conditionIdList)

																	#This would be a lot simpler if Data_API.get_trades() accurately took list of conditionIds

																	#To work around we need output List[Dict] of all suspicious trades 

DataTest = api.Data_API()											# start data session

all_trades = [] # -> List[List[Dict]]	

print("Fetching trades... (rate limited)")
for conditionId in conditionIdList:									# append to list List[Dict] for trades of ech conditionId
	#time.sleep(0.0)
	all_trades.append(DataTest.get_trades(market=conditionId, limit=1000)) 


outliers = []

print("Filtering outliers")
for market_trades in all_trades: 									#append to list List[Dict] basic outlier check
	outliers.append(trademath.Trade(market_trades=market_trades))	#Init trades, filter, average, z score


final_list =[]

print("Doing statistical analysis")
for outlier in outliers: 
	outlier.time_analysis(event_data_list=event_data_list)			#Run time analysis on each trade object
	outlier.confidence_analysis()									#Final stats
	for trade in outlier.market_trades: 
		if trade["confidenceValue"] > 0.55:
			final_list.append(trade)								#Only the strongest survive

len_before_culling = len(final_list)
final_list = [dict(t) for t in {tuple(sorted(d.items())) for d in final_list}]	#Flatten
print(f"Total: {len_before_culling}, Cut: {len_before_culling-len(final_list)}, Remaining: {len(final_list)}")	

final_list.sort(key=lambda x: x["timeRemainingUTC"],)#reverse=True) #Sort by time remaining 


with open("output.json", "w") as f:
	json.dump(final_list, f, indent=2)				#Output json

print("done")
