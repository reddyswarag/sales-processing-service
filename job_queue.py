from redis import Redis
from rq import Queue

redis_connection = Redis(host = "localhost", port = 6379, db = 0)

csv_queue = Queue("csv", connection= redis_connection)
