from marshmallow import Schema, fields


class TokenSchema(Schema):
    claims = fields.Str()
    class Meta:
        strict = True


class RunSchema(Schema):
    token = fields.Nested(TokenSchema)
    scenario = fields.Str()
    user = fields.Str()
    name = fields.Str(required=False)
    format = fields.Str(default='.sqlite', required=False)
    class Meta:
        strict = True


class CancelSchema(Schema):
    token = fields.Nested(TokenSchema)
    jobid = fields.Str()
    class Meta:
        strict = True

    
class StatusSchema(Schema):
    token = fields.Nested(TokenSchema)
    jobid = fields.Str()
    class Meta:
        strict = True

