import requests
from py_clob_client.client import ClobClient, OrderBookSummary
from py_clob_client.clob_types import BookParams
from typing import Dict, List
import time

BASE_URL_GAMMA = "https://gamma-api.polymarket.com/"
BASE_URL_CLOB = "https://clob.polymarket.com/"
BASE_URL_DATA = "https://data-api.polymarket.com/"


'''
Class: Gamma_API
Description: Upon initializing begins web session, returns queries through methods
Methods: get_markets, fetch_by_slug, get_markets_by_pagination
'''
class Gamma_API:
	def __init__(self):
		self.session = requests.Session()

	def get_markets(self, tag_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
		resp = self.session.get(
			f"{BASE_URL_GAMMA}events?",
			params = {
				"tag_id" : tag_id,
				"limit": limit,
				#"active": True,
				"closed": False,
			}
		)

		resp.raise_for_status()
		return resp.json()

	def fetch_by_slug(self, slug:str):
		resp = self.session.get(
			f"{BASE_URL_GAMMA}events/slug/{slug}"
			)
		resp.raise_for_status()
		return resp.json()

	def get_markets_by_pagination(self,tag_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
		listed_pages = []
		time.sleep(0.25) 		#Primitive rate limiting
		for i in range(offset):
			page = self.session.get(
				f"{BASE_URL_GAMMA}events?",
				params = {
					"tag_id" : tag_id,
					"limit" : limit,
					"closed": False,
					"active": True,
					"offset": i
				}
				)
			page.raise_for_status()
			listed_pages.append(page.json())

		return [conditionId for page in listed_pages for conditionId in page]

	def get_event_data(self, markets: List[Dict]) -> List[Dict]:
		ids_slugs_dicts = []
		for market in markets:
			for event in market["markets"]:
				if event["closed"]==True:
					break
				ids_slugs_dicts.append({"conditionId" : event["conditionId"], "slug":event["conditionId"], "endDate":event["endDate"]})
		return ids_slugs_dicts



	def end_session(self):
		self.session.close()

'''
Class: Clob_API
Description: Upon initializing begins web session, returns queries through methods
Methods: event_data, tokens, retrieve_bids
Note: not really relevent unless headless orders are to be made
'''

class Clob_API: #Prices, orderbooks, trading
	def __init__(self):
		self.client = ClobClient(
			host=BASE_URL_CLOB,
			chain_id=137
		)

	def event_data(self, conditionId: str):
		return self.client.get_market(conditionId)

	def tokens(self, eventData: Dict) -> List[Dict]:
		self.eventData = eventData 
		return self.eventData["tokens"] # ->
		

	def retrieve_bids(self, OrderBookSummary: OrderBookSummary) -> List[Dict]:
		bids = []
		for bid in OrderBookSummary.bids:
			bids.append({"price": bid.price, "size": bid.size})
		return bids




''' 
def market_filter(markets: list[dict], topics: List[str]) -> List[str]: #maybe change return for ease later, this list will have to be used by later classes to cross ref ID,
	desired_markets = []											

	for market in markets:
		for topic in topics:
			if topic in market["title"].lower(): # & os.time.laterthan(market["end_date?"]) != True 
				for event in market["markets"]:
					#print(event)
					try:
						#print(f"{event["question"]}\n\tconditionId: {event["conditionId"]}")
						desired_markets.append(event["conditionId"])
						break
					except:
						print(f"Missing data...")
						break


	return desired_markets
'''

'''
Class: Data_API
Description: Upon initializing begins web session, returns queries through methods
Methods: get_trades, 
'''

class Data_API: #Positions, activity, history  
	def __init__(self):
		self.session = requests.Session()

	def get_trades(self, market: List[str], takerOnly=True, limit = 1000) -> List[Dict]: # market has to be list of conditionIds but list doesn't seem to work
		resp = self.session.get(														# passing single conditionIds does though
			f"{BASE_URL_DATA}trades?",
			params = {
				"market" : market,
				"takerOnly" : takerOnly,
				"limit" : limit
				}
			)

		resp.raise_for_status()
		return resp.json()


	