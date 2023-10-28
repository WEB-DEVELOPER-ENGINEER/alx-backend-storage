#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


if __name__ == "__main__":
    """provides some stats about Nginx logs stored in MongoDB"""
    with MongoClient() as client:
        db = client.logs
        collection = db.nginx

        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        method_stats = []

        for method in methods:
            method_count = collection.count_documents({'method': method})
            method_stats.append({'method': method, 'count': method_count})

        doc_count = collection.estimated_document_count()
        status_path_stats = collection.count_documents({'method': 'GET', 'path': '/status'})

    return doc_count, method_stats, status_path_stats


def print_nginx_stats() -> None:
    """
    Prints stats from the nginx query.
    """
    doc_count, method_stats, status_path_stats = get_nginx_stats()

    print(f'{doc_count} logs')
    print('Methods:')
    for method in method_stats:
        print(f'\tmethod {method["method"]}: {method["count"]}')
    print(f'{status_path_stats} status check')


if __name__ == '__main__':
    print_nginx_stats()
