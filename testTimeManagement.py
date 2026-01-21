def word_search(markets: list[dict], topics: List[str]) -> List[str]: #maybe change return for ease later, this list will have to be used by later classes to cross ref ID
	desired_markets = []

	for market in markets:
		for topic in topics:
			if topic in market["title"].lower(): # & os.time.laterthan(market["end_date?"]) != True 
				for event in market["markets"]:
					try:
						endTime = datetime.fromisoformat(event["endDate"].replace("Z","+00:00")).astimezone(timezone.utc)


						if datetime.utcnow() < endTime:

							print(f"{event["question"]}\n\tconditionId: {event["conditionId"]}")
							desired_markets.append(event["conditionId"])
							break
						else: 

							print("Market expired...")

					except:
						print(f"Missing data...")
						break

	return desired_markets
