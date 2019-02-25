from flask import Blueprint
from flask_restplus import Api, Resource
from webargs.flaskparser import use_args, use_kwargs

from .schema import RunSchema, CancelSchema, StatusSchema
from . import jobs

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Recyclus simulation service',
          version='1.0',
          description='Remote cyclus simulation services api',
          doc='/doc/')


@api.route('/run')
class Run(Resource):
    @use_kwargs(RunSchema())
    def post(self, token, **kwargs):
        print('run: ', token, kwargs)
        return jobs.create(kwargs)
        # return 'ok'


@api.route('/cancel/<jobid>')
# @use_kwargs(CancelSchema())
class Cancel(Resource):

    @use_kwargs(CancelSchema())
    def delete(self):
        return 'ok'


@api.route('/status/<jobid>')
# @use_kwargs(StatusSchema())
class Status(Resource):

    # @use_kwargs(StatusSchema())
    def get(self, jobid):
        print('status of', jobid)
        return 'ok'

