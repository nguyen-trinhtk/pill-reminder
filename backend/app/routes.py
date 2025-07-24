from flask import Blueprint, request, jsonify
from .db.db_client import get_client, close_client
from .db.users import create_user, read_user, update_user, delete_user
from .db.prescriptions import create_prescription, read_prescriptions, delete_prescription, update_prescription

bp = Blueprint('api', __name__)

@bp.route('/users', methods=['POST'])
def api_create_user():
    data = request.json
    client = get_client()
    try:
        user_id = create_user(client, data['name'], data['dob'], data['email'])
        return jsonify({'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    client = get_client()
    try:
        user = read_user(client, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/users/<user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.json
    client = get_client()
    try:
        updated = update_user(client, user_id, data.get('name'), data.get('dob'), data.get('email'))
        return jsonify({'updated': updated})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/users/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    client = get_client()
    try:
        deleted = delete_user(client, user_id)
        return jsonify({'deleted': deleted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/users/<user_id>/prescriptions', methods=['POST'])
def api_add_prescription(user_id):
    data = request.json
    client = get_client()
    try:
        presc_id = create_prescription(
            client, user_id,
            data['medication'],
            data['dosage'],
            data['instructions'],
            data['frequency'],
            data['time']
        )
        return jsonify({'prescription_id': presc_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/users/<user_id>/prescriptions', methods=['GET'])
def api_get_prescriptions(user_id):
    client = get_client()
    try:
        prescriptions = read_prescriptions(client, user_id)
        return jsonify(prescriptions)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/prescriptions/<presc_id>', methods=['DELETE'])
def api_delete_prescription(presc_id):
    client = get_client()
    try:
        deleted = delete_prescription(client, presc_id)
        return jsonify({'deleted': deleted})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)

@bp.route('/prescriptions/<presc_id>', methods=['PUT'])
def api_update_prescription(presc_id):
    data = request.json
    client = get_client()
    try:
        updated = update_prescription(
            client, presc_id,
            data.get('medication'),
            data.get('dosage'),
            data.get('instructions'),
            data.get('frequency'),
            data.get('time')
        )
        return jsonify({'updated': updated})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        close_client(client)
