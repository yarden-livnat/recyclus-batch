import os
from redis import Redis

cache = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)


def next_jobid():
    return f"job:{cache.incr('job_counter')}"


def create(req):
    id = next_jobid()
    job = {
        'id': id,
        'scenario': req['scenario'],
        'user': req['user'],
        'name': req['name'],
        'status': 'pending'
    }
    cache.hmset(id, job)
    cache.lpush('q:submit', job['id'])
    return job


def status(req):
    return cache.hmget(req['jobid'], 'status')

