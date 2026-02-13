import api
import trademath
import json
from typing import List, Dict


TAG_IDS = {
	"politics": "2",
	"geopolitics": "100265"

}

TOPICS_WE_LIKE = ["greenland", "venezuela", "iran", "israel" ]      #check for spelling errors lol, always lowercase

GammaTest = api.Gamma_API() 										# start gamma session, create gamma object for access to methods

markets = GammaTest.get_markets_by_pagination(tag_id=TAG_IDS["geopolitics"], offset=25)  # pull markets from api using gamma object

print("fetching markets")
conditionIdList = api.market_filter(markets, TOPICS_WE_LIKE)		# filter for keywords and return list of conditionIds to be used with clob, prints each approved market
print(f"# MARKETS SEARCHED: {len(conditionIdList)}")

																	#This would be a lot simpler if Data_API.get_trades() accurately took list of conditionIds

																	#To work around we need output List[Dict] of all suspicious trades 

DataTest = api.Data_API()											# start data session

all_trades = [] # -> List[List[Dict]]	

for conditionId in conditionIdList:	
	print(f"fetching trades for {conditionId}")								# append to list List[Dict] for trades of ech conditionId
	all_trades.append(DataTest.get_trades(market=conditionId, limit=10000))



outliers = []

for market_trades in all_trades: 									#append to list List[Dict] basic outlier check
	print("Filtering outliers")
	outliers.append(trademath.Trades(market_trades=market_trades))	#Do a bunch of shit on init of Trades



final_list =[]

for outlier in outliers: 
	#print(outlier.market_trades)
	print("Doing statistical analysis")									# Do a bunch of shit 
	outlier.time_analysis(Gamma_API=GammaTest)
	outlier.confidence_analysis()
	for trade in outlier.market_trades: 
		if trade["confidenceValue"] > 0.55:
			final_list.append(trade)								# Ta-Da



final_list.sort(key=lambda x: x["confidenceValue"], reverse=True) 


with open("output.json", "w") as f:
	json.dump(final_list, f, indent=2)

print("done")


