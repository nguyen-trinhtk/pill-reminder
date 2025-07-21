from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

@main.route('/dispense', methods=['POST'])
def dispense():
    data = request.get_json()
    # Example: Log to database or perform action
    return jsonify({"message": "Pill dispensed"}), 200