import os
import json
import time
import datetime
from utils.logger import log_to_csv

def update_knowledge_base(weather, co2, calendar, dht_data):
    print("\n Updating knowledge base at {}".format(time.time()))
    timestamp = time.time()
    timestamp_human = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    knowledge = {
        "timestamp": timestamp,
        "timestamp_human": timestamp_human,
        "dht_data": dht_data,
        "weather": weather,
        "co2": co2,
        "calendar": calendar
    }

    os.makedirs("knowledge", exist_ok=True)

    # Save knowledge base as JSON
    with open("knowledge/knowledge_base.json", "w") as f:
        json.dump(knowledge, f, indent=4)
        print("knowledge/knowledge_base.json updated")

    # Log to CSV
    log_to_csv(knowledge)
    print(" Appended to knowledge_log.csv")
