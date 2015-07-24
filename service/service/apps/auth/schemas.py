from cornice.schemas import CorniceSchema
from colander import MappingSchema, SchemaNode, String, drop


class AuthSchema(MappingSchema):
    email = SchemaNode(String(), location='body', type='str')
    password = SchemaNode(String(), location='body', type='str')

class NewUserSchema(MappingSchema):
    email = SchemaNode(String(), location='body', type='str')
    password = SchemaNode(String(), location='body', type='str')

class UserSchema(MappingSchema):
    id = SchemaNode(String(), location='body', type='str')
    email = SchemaNode(String(), location='body', type='str')
    password = SchemaNode(String(), location='body', type='str')
