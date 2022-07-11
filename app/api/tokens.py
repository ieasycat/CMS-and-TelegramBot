from app import db
from app.api import bp
from app.api.authorization import auth
from flask import jsonify, g


@bp.route('/tokens', methods=['POST'])
@auth.login_required
def get_token():
    token = g.user.get_token()
    db.session.commit()
    return jsonify({'token': token})
