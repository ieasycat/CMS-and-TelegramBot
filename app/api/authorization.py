from app.models.dbmodels import Manager
from app.api import auth
from flask import g


@auth.verify_password
def verify_password(email: str, password: str) -> bool:
    user = Manager.query.filter_by(email=email).first()
    if not user or not user.check_password(password=password):
        return False
    g.user = user
    return True
