from flask import Blueprint, request, current_app as app
from flask_restplus import Api, Resource
import requests
from webargs.flaskparser import use_args

from .schema import cancel_args, delete_args, run_args
from . import jobs
from .exceptions import BatchException

datastore = 'http://datastore:5020/api/internal'

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Recyclus simulation service',
          version='1.0',
          description='Remote cyclus simulation services api',
          doc='/doc/')


@api.route('/run')
class Run(Resource):
    @use_args(run_args)
    def post(self, args):
        identity = args.pop('identity')
        if args.get('user') is None:
            args['user'] = identity['user']
        job = jobs.create(args['user'], args['project'], args['tasks'])
        jobs.schedule(job)
        return {
            'jobid': job['jobid'],
            'project': job['project']
        }


@api.route('/cancel/<jobid>')
class Cancel(Resource):

    @use_args(cancel_args)
    def delete(self, args, jobid):
        try:
            return {'status': 'ok', 'message' : jobs.cancel(jobid, args['identity']['user'])}
        except BatchException as e:
            return {'status': 'error', 'messsage' : e.message}


@api.route('/status/<jobid>')
class Status(Resource):

    # @use_kwargs(StatusSchema())
    def get(self, jobid):
        try:
            info = jobs.status(jobid)
            return {'status': 'ok', 'info' : info}
        except BatchException as e:
            return {'status': 'error', 'message': e.message}


@api.route('/delete/<jobid>')
class Delete(Resource):

    @use_args(delete_args)
    def delete(self, args, jobid):
        try:
            jobs.delete(jobid, args['identity']['user'])
            requests.delete(f'{datastore}/delete', json={'jobid': jobid})
            return {'status': 'ok'}
        except BatchException as e:
            return {'status': 'ok', 'message': e.message}
