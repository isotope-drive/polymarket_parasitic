from typing import List,Dict
import api
import statistics
from datetime import datetime, timedelta
# import numpy as np
# import math

class Trade:
	def __init__(self,market_trades: List[Dict]):

		self.kill_list = ["icon","bio","profileImage","profileImageOptimized"]

		self.market_trades = market_trades
		self.average_trades()
		self.outliers()
		self.price_analysis()
		
		#self.time_analysis()



	def average_trades(self): #Also performs cleaning
		values = {"BUY": [], "SELL": []}

		for trade in self.market_trades:
			self.local_tv = trade["value"] = trade["size"]*trade["price"]
			values[trade["side"]].append(self.local_tv)

			for key in self.kill_list:
				trade.pop(key, None)

		self.buy_mean = statistics.mean(values["BUY"]) if values["BUY"] else 0
		self.buy_sd = statistics.pstdev(values["BUY"]) if values["BUY"] else 0

		self.sell_mean = statistics.mean(values["SELL"]) if values["SELL"] else 0
		self.sell_sd = statistics.pstdev(values["SELL"]) if values["SELL"] else 0
		
	#def threshold(self, n:int):
	# return max(3.0, 2.0 + math.log10(n)) This will give us the threshold for our z-score with 99% confidence

	#def outliers(self, threshold:float): Helps cut out the z_score calculation. Also allows for the threshold to change if there are too mnay trades.
	# outliers = []
	# trades = 0
	# 
	# for trade in self.market_trades:
	#	trades++
	# z_score = (trades - buy_mean) / buy_sd
	# z_score_sell = (trades - sell_mean) / sell_sd
	#	if (np.abs(z_score) > threshold or np.abs(z_score_sell) > threshold):
	#		outliers.append(trade)
	# return outliers

	def outliers(self):
		outliers = []

		for trade in self.market_trades:
			if trade["side"] == "BUY":

				if (trade["value"]-self.buy_mean) > (2*self.buy_sd):
					outliers.append(trade)

			else:
				if (trade["value"]-self.sell_mean) > (2*self.sell_sd):
					outliers.append(trade)

		self.market_trades = outliers #ok ok ok maybe not 

	def price_analysis(self):
		for trade in self.market_trades:
			if trade["side"] == "BUY":
				trade["zScore"] = self.z_score_calculation(trade, "buy")
			if trade["side"] == "SELL":
				trade["zScore"] = self.z_score_calculation(trade, "sell")
			#else: detonate CPU


	def z_score_calculation(self,trade,side:str):
		mean = getattr(self, f"{side}_mean")
		sd = getattr(self, f"{side}_sd")
		if sd <= 0:
			return 0.0 						#Zeros must be handled
		return (trade["value"]-mean)/sd

	def time_analysis(self, event_data_list: List):
		for trade in self.market_trades:
			this_conditionId = trade["conditionId"]
			for event in event_data_list:
				if this_conditionId == event["conditionId"]:
					end_date = event["endDate"]
					end_date = datetime.fromisoformat(end_date.replace("Z","+00:00"))
					end_date = int(datetime.timestamp(end_date))

					time_remaining = end_date - trade["timestamp"]

					trade["timeRemainingUTC"] = time_remaining
					trade["timeRemainingHuman"] = str(timedelta(seconds=time_remaining))
					trade["endDate"] = end_date

					break

	def confidence_analysis(self):


		for trade in self.market_trades:
			time_weight = 0
			value_weight = 0

			if trade["endDate"] == 'Unknown':
				time_weight = 0.0
			else:
				time_weight = 0.0

			value_weight = (trade["zScore"]/10) + (trade["value"]/10000)

			trade["confidenceValue"] = 	(value_weight*1.0) + (time_weight*0.0)


'''
	def time_analysis(self, Gamma_API: api.Gamma_API):
		slug_cache = {}

		for trade in self.market_trades:
			try:
				slug = trade["slug"]

				if slug not in slug_cache:
					slug_cache[slug] = Gamma_API.fetch_by_slug(slug=slug)

				end_date = slug_cache[slug]["endDate"]#Gamma_API.fetch_by_slug(slug=trade["slug"])["endDate"]
				end_date = datetime.fromisoformat(end_date.replace("Z","+00:00"))
				end_date = int(datetime.timestamp(end_date))

				time_remaining = end_date - trade["timestamp"]

				trade["timeRemainingUTC"] = time_remaining
				trade["timeRemainingHuman"] = str(timedelta(seconds=time_remaining))
				trade["endDate"] = end_date

			except Exception as ex:

				trade["timeRemainingUTC"] = 'Unknown'
				trade["timeRemainingHuman"] = 'Unknown'
				trade["endDate"] = 'Unknown'
'''
