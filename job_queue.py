from redis import Redis
from rq import Queue
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


redis_connection = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

csv_queue = Queue("csv", connection=redis_connection)