#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


if __name__ == "__main__":
    """provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient()
    nginx_collection = client.logs.nginx
    nginx_logs = nginx_collection.count_documents({})
    print(f'{nginx_logs} logs')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f'{status_check} status check')
