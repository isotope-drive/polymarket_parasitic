from typing import List,Dict
import statistics

def average_trades(market_data: List[Dict]) -> List[Dict]:
	buys = {"buys": []}
	sells = {"sells": []}

	for activity in market_data: 
		if activity["side"] == "BUY":
			buys["buys"].append(activity["size"]*activity["price"])
		elif activity["side"] == "SELL":
			sells["sells"].append(activity["size"]*activity["price"])

	buys["buys_mean"] = statistics.mean(buys["buys"])
	sells["sells_mean"] = statistics.mean(sells["sells"])

	buys["buys_sd"] = statistics.pstdev(buys["buys"])
	sells["sells_sd"] = statistics.pstdev(sells["sells"])

	buys.pop("buys",None)
	sells.pop("sells",None)
	return [buys, sells]


#find mean
#find sd
#check sd against purchases to find outliers
#return specific List[Dict] of interesting trades


def outliers(market_data: List[Dict], market_info: List[Dict], buys=True) -> List[str]:
	if buys == True:
		working_set = market_info[0]
	else:
		working_set = market_info[1]



#This code really really sucks dick i think. There is a massivly better recursive 
#or some shit way to retrieve the mean data and then the sd data. 