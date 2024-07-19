#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB.
Database: logs, Collection: nginx.

The output includes:
- The number of logs
- The count of each HTTP method (GET, POST, PUT, PATCH, DELETE)
- The count of status checks (method=GET, path=/status)
- The top 10 most present IPs
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Provides statistics about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: pymongo collection object.
    """
    # Total number of logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count of each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count of status checks
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Top 10 most present IPs
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    for ip in mongo_collection.aggregate(pipeline):
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    log_stats(nginx_collection)

