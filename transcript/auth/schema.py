from transcript.auth.models import User
from transcript.ext import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        include_relationship = True
