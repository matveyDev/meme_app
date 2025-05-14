from fastapi import Request, HTTPException
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
IP_LIMIT = 2

def check_and_update_ip_limit(request: Request, wallet_limit: int):
    if wallet_limit > IP_LIMIT:
        return
    ip = request.client.host
    key = f"ip_limit:{ip}"
    current = redis_client.get(key)
    ip_count = int(current) if current else 0
    if ip_count >= IP_LIMIT:
        raise HTTPException(status_code=429, detail="IP generation limit reached.")
    redis_client.incr(key)
