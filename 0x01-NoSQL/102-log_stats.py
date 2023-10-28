#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient

def print_results(title, results):
    """Print the results with a title."""
    print(title)
    for result in results:
        print(f'\t{result["label"]}: {result["count"]}')

if __name__ == "__main__":
    # Provides some stats about Nginx logs stored in MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_results = [
        {"label": method, "count": nginx_collection.count_documents({"method": method})}
        for method in methods
    ]
    print_results('Methods:', method_results)

    status_check = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f'{status_check} status check')

    top_ips = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    top_ip_results = [
        {"ip": top_ip.get("ip"), "count": top_ip.get("count")}
        for top_ip in top_ips
    ]
    print_results('IPs:', top_ip_results)
