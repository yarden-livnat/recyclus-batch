import json
from redis import Redis
from flask import current_app as app

from .exceptions import BatchException

cache = Redis(host='redis', db=0, decode_responses=True, socket_connect_timeout=2, socket_timeout=2)


def create_jobid(user, project):
    counter = f'counter:{user}:{project}'
    n = cache.incr(counter)
    return f'{user}:{project}-{n}'


def job_key(jobid):
    return f'job:{jobid}'


def schedule(job):
    cache.lpush('q:submit', job['key'])


def create(user, project, tasks):
    jobid = create_jobid(user, project)
    key = job_key(jobid)

    job = {
        'jobid': jobid,
        'key': key,
        'user': user,
        'project': project,
        'status': 'pending',
        'tasks': json.dumps(tasks),
        'logid': f'{key}:log'
    }
    cache.hmset(key, job)

    app.logger.debug('job created')
    return job


def status(jobid):
    key = job_key(jobid)
    if cache.exists(key):
        info = {
            'status': cache.hget(key, 'status')
        }

        record = cache.hgetall(f'{key}:status:simulation')
        if record:
            info['simulation'] = record

        record = cache.hgetall(f'{key}:status:post')
        if record:
            info['post'] = record

        return info
    else:
        raise BatchException(f'unknown job {jobid}')


def cancel(jobid, user):
    key = job_key(jobid)
    if cache.exists(key):
        if cache.hget(key, 'user') != user:
            raise BatchException(f'no such job for user:{user}')

        # todo: race condition
        job_status = cache.hget(key, 'status')

        if job_status == 'pending':
            r = cache.lrem('q:submit', -1, key)
            app.logger.debug('remove=', r)
            cache.delete(key)
            return 'canceled'

        if job_status.startswith('running'):
            cache.hset(key, 'ctrl', 'cancel')
            return 'cancel scheduled'

        BatchException(f'job "{jobid}" is not running')
    else:
        BatchException('unknown job')


def delete(jobid, user):
    key = job_key(jobid)
    if cache.exists(key):
        if cache.hget(key, 'user') != user:
            BatchException(f'no such job for user:{user}')

        job_status = cache.hget(key, 'status')
        if job_status not in ['done', 'failed', 'canceled']:
            BatchException('can not delete a running job')

        keys = cache.keys(f'{key}:*') or []
        app.logger.debug('delete keys: %s', str(keys))
        keys.append(key)
        cache.delete(*keys)
    else:
        BatchException(f'unknown job {jobid}')


