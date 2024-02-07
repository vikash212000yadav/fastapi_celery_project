from celery import Celery
import time
import math

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@celery.task
def get_primes(n, delay=0):
    if delay > 0:
        time.sleep(delay)

    if n < 1:
        return []
    primes = [2]
    num = 3
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p > math.sqrt(num):
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 2
    return primes
