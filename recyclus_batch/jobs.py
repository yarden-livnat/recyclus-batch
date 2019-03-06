from redis import Redis
from flask import current_app as app

cache = Redis(host='redis', db=0, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)
pubsub = cache.pubsub()


def create_jobid(user, name):
    counter = f'counter:{user}:{name}'
    n = cache.incr(counter)
    return f'{user}:{name}-{n}'


def job_key(jobid):
    return f'job:{jobid}'


def create(req):
    user = req['user']
    name = req['name']
    jobid = create_jobid(user, name)
    key = job_key(jobid)

    job = {
        'jobid': jobid,
        'key': key,
        'user': user,
        'name': name,
        'status': 'pending'
    }
    cache.hmset(key, job)
    cache.hmset(f'{key}:sim', req['simulation'])

    cache.lpush('q:submit', key)
    return job


def status(jobid):
    key = job_key(jobid)
    if cache.exists(key):
        info = {
            'jobid': jobid,
            'status': cache.hget(key, 'status')
        }
        if info['status'] == 'failed':
            info['error'] = cache.hget(key, 'error')
        return info
    else:
        return {
            'jobid': jobid,
            'status': 'unknown job'
        }


def cancel(jobid, user):
    key = job_key(jobid)
    if cache.exists(key):
        if cache.hget(key, 'user') != user:
            return {'message': f'no such job for user:{user}'}

        status = cache.hget(key, 'status')

        if status == 'pending':
            r = cache.lren('q:submit', -1, key)
            app.logger.debug('remove=', r)
            cache.delete(key)
            return {'message': 'canceled'}

        if status.startswith('running'):
            cache.hset(key, 'ctrl', 'cancel')
            # cache.publish('cancel-job', jobid)
            app.logger.debug('published cancel job %s', jobid)
            return 'cancel scheduled'

        return {'message': f'job "{jobid}" is not running'}
    else:
        return {
            'jobid': jobid,
            'status': 'unknown job'
        }
