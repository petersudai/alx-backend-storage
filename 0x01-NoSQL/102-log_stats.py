#!/usr/bin/env python3
"""
Log Stats Script
This script provides statistics about Nginx logs stored in MongoDB.
top 10 most present IPs
"""

from pymongo import MongoClient


def log_stats():
    """
    Connects to the MongoDB server, retrieves log statistics
    from the 'logs' database
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count the number of documents
    count_logs = collection.count_documents({})

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Count the number of documents with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Print the results
    print(f"{count_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check_count} status check")

    # Aggregation pipeline to find the top 10 most present IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(collection.aggregate(pipeline))

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
