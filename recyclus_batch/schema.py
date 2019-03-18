from webargs import fields

identity_args = {
    'user': fields.Str(required=True),
    'roles': fields.Str(required=True)
}

sim_args = {
    'scenario': fields.Str(required=True),
    'scenario_filename': fields.Str(),
    'format': fields.Str(missing='sqlite'),
    'files': fields.List(fields.Str())
}

post_args = {
    'script': fields.Str(required=True),
    'scenario_filename': fields.Str(),
    'files': fields.List(fields.Str())
}

tasks_args = {
    'simulation': fields.Nested(sim_args, required=True),
    'post': fields.Nested(post_args)
}

run_args = {
    'identity': fields.Nested(identity_args, required=True),
    'user': fields.Str(),
    'project': fields.Str(missing='default'),
    'tasks': fields.Nested(tasks_args, required=True)
}


cancel_args = {
    'identity': fields.Nested(identity_args, required=True)
}

delete_args = {
    'identity': fields.Nested(identity_args, required=True)
}