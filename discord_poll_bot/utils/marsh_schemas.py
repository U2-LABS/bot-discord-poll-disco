from marshmallow import Schema, fields


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = CamelCaseSchema.camelcase(field_obj.data_key or field_name)

    @staticmethod
    def camelcase(field):
        parts = iter(field.split("_"))
        return next(parts) + "".join(part.title() for part in parts)

    class Meta:
        ordered = True


class SongSchema(CamelCaseSchema):
    id_music = fields.Int(required=True)
    title = fields.Raw(required=True)
    author = fields.Raw(required=True)
    link = fields.Url(required=True)
    mark = fields.Int(required=True)
    pos = fields.Int(required=True)
    voted_users = fields.List(fields.Int())


class StateSchema(CamelCaseSchema):
    chat_id = fields.Int(allow_none=True)
    count_music = fields.Int(required=True)
    message_id = fields.Int(allow_none=True)
    poll_started = fields.Bool(required=True)
    users_for_promoting = fields.List(fields.Str())
    upload_flag = fields.Bool(required=True)
    top_songs = fields.List(fields.Nested(SongSchema))
