from flask import Blueprint, jsonify, request
from flask import current_app as eos
import logging

logger = logging.getLogger(__name__)

tickets = Blueprint('tickets', __name__)

@tickets.route('/tickets', methods=['GET'])
@tickets.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id=None):
    """
    Retrieve tickets from the database.

    :param ticket_id: Optional integer ID of a specific ticket
    :return: JSON response with ticket(s)
    """
    try: 
        if ticket_id is None:
            # Retrieve all tickets
            result = eos.db.get_tickets()
        else:
            # Retrieve a single ticket
            result = eos.db.get_ticket(ticket_id)
    except Exception as e:
        logger.error(f"Error retrieving ticket(s) from database: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while retrieving tickets.'}), 500

    return jsonify(result), 200

@tickets.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    """
    Update an existing ticket in the database.
    """
    if request.method == 'PUT':
        data = request.json
        try:
            result = eos.db.update_ticket_status(int(ticket_id), data['status'])
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error updating ticket in database: {e}")
            return jsonify({'status': 'error', 'message': 'An error occurred while updating the ticket.'}), 500

    return jsonify({'message': 'improper request method'}), 405

@tickets.route('/tickets', methods=['POST'])
def add_ticket():
    """
    Add a new ticket to the database.
    """
    if request.method == 'POST':
        data = request.json
        try:
            result = eos.db.add_ticket(data)
            return jsonify(result), 201
        except Exception as e:
            logger.error(f"Error adding ticket to database: {e}")
            return jsonify({'status': 'error', 'message': 'An error occurred while adding the ticket.'}), 500

    return jsonify({'message': 'improper request method'}), 405

@tickets.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """
    Delete a specific ticket from the database.
    """
    if request.method == 'DELETE':
        try:
            result = eos.db.delete_ticket(ticket_id)
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error deleting ticket from database: {e}")
            return jsonify({'status': 'error', 'message': 'An error occurred while deleting the ticket.'}), 500

    return jsonify({'message': 'improper request method'}), 405
