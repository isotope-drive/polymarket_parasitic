from typing import List,Dict
import api
import statistics
from datetime import datetime, timedelta

class Trades:
	def __init__(self,market_trades: List[Dict]):
		self.market_trades = market_trades
		self.average_trades()
		self.outliers()
		self.price_analyisis()
		
		#self.time_analyisis()



	def average_trades(self):
		values = {"BUY": [], "SELL": []}

		for trade in self.market_trades:
			local_tv = trade["value"] = trade["size"]*trade["price"]
			values[trade["side"]].append(local_tv)
		
		self.buy_mean = statistics.mean(values["BUY"])
		self.buy_sd = statistics.pstdev(values["BUY"])

		self.sell_mean = statistics.mean(values["SELL"])
		self.sell_sd = statistics.pstdev(values["SELL"])
		

	def outliers(self):
		outliers = []

		for trade in self.market_trades:
			if trade["side"] == "BUY":
				if (trade["value"]-self.buy_mean) > (2*self.buy_mean):
					outliers.append(trade)
			else:
				if (trade["value"]-self.sell_mean) > (2*self.sell_mean):
					outliers.append(trade)

		self.market_trades = outliers #ok ok ok maybe not :P

	def price_analyisis(self):
		for trade in self.market_trades:
			if trade["side"] == "BUY":
				trade["Z_SCORE"] = self.z_score_calculation(trade, "buy")
			if trade["side"] == "SELL":
				trade["Z_SCORE"] = self.z_score_calculation(trade, "sell")


	def z_score_calculation(self,trade,side:str):
		trade_value = trade["size"]*trade["price"]
		mean = getattr(self, f"{side}_mean")
		sd = getattr(self, f"{side}_sd")
		return (trade_value-mean)/sd 

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
				#print(ex)
				trade["timeRemainingUTC"] = 'Unknown'
				trade["timeRemainingHuman"] = 'Unknown'
				trade["endDate"] = 'Unknown'


	def confidence_analysis(self):


		for trade in self.market_trades:
			timeWeight = 0
			valueWeight = 0

			if trade["endDate"] == 'Unknown':
				timeWeight = 0.0
			else:
				timeWeight = 0.0

			valueWeight = (trade["Z_SCORE"]/10) + (trade["value"]/10000)

			trade["confidenceValue"] = (valueWeight*1.0) + (timeWeight*0.0)



