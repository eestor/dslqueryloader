from flask import Blueprint, render_template, abort, jsonify
from src.controllers.decorators import admin_required, permission_required
from src.models.ds_schema import DsSchema
from src.models.permission import Permission
from flask_login import login_required, current_user

schemas = Blueprint('schemas', __name__)

@schemas.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@schemas.route('/schema/<id>')
def schema_data(id):
    schema = DsSchema.query.get_or_404(id)
    if not schema:
        abort(404)
    return jsonify(schema)
    # return render_template('schema.html', schema=schema)


@schemas.route('/permission/admin')
@login_required
@admin_required
def admin():
    return str(current_user.is_administrator())


@schemas.route('/permission/user')
@permission_required(Permission.READ)
def moderator():
    return str(current_user.is_administrator())
