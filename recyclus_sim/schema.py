from webargs import fields

identity_args = {
    'user': fields.Str(required=True),
    'roles': fields.Str(required=True)
}

sim_args = {
    'scenario': fields.Str(required=True),
    'scenario_filename': fields.Str(),
    'format': fields.Str(missing='sqlite')
}

run_args = {
    'identity': fields.Nested(identity_args, required=True),
    'user': fields.Str(),
    'name': fields.Str(missing='default'),
    'simulation': fields.Nested(sim_args, required=True)
}
