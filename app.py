from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import urllib.parse

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        username = "postgres"
        password = urllib.parse.quote_plus("root")
        host = "localhost"
        port = 5432
        database_name = "parking_db"

        # Set the SQLAlchemy database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # MODELS
    class ParkingData(db.Model):
        __tablename__ = 'parking_data'
        parking_name = db.Column(db.String(255), primary_key=True)
        city = db.Column(db.String(255), nullable=False)
        parking_location = db.Column(db.String(255), nullable=False)
        address_1 = db.Column(db.Text)
        address_2 = db.Column(db.Text)
        latitude = db.Column(db.Float)
        longitude = db.Column(db.Float)
        physical_appearance = db.Column(db.String(255))
        parking_ownership = db.Column(db.String(255))
        parking_surface = db.Column(db.String(255))
        has_cctv = db.Column(db.String(255))
        has_boom_barrier = db.Column(db.String(255))
        ticket_generated = db.Column(db.String(255))
        entry_exit_gates = db.Column(db.String(255))
        weekly_off = db.Column(db.String(255))
        parking_timing = db.Column(db.String(255))
        vehicle_types = db.Column(db.String(255))
        car_capacity = db.Column(db.Integer)
        two_wheeler_capacity = db.Column(db.Integer)
        parking_type = db.Column(db.String(255))
        payment_modes = db.Column(db.String(255))
        car_parking_charge = db.Column(db.String(255))
        two_wheeler_parking_charge = db.Column(db.Text)
        allows_prepaid_passes = db.Column(db.String(255))
        provides_valet_services = db.Column(db.String(255))
        value_added_services = db.Column(db.String(255))
        notes = db.Column(db.String(255))
        total_slots = db.Column(db.Integer)
        available_slots = db.Column(db.Integer)
        parking_id = db.Column(db.Integer)
    
    class Parkinglots(db.Model):
        __tablename__ = 'parkinglots_Details'
        id = db.Column(db.Integer, primary_key=True)
        parking_id = db.Column(db.Integer)
        parking_name = db.Column(db.String(255))
        city = db.Column(db.String(100))
        parking_location = db.Column(db.String(255))
        address_1 = db.Column(db.Text)
        address_2 = db.Column(db.Text)
        latitude = db.Column(db.Float)
        longitude = db.Column(db.Float)
        physical_appearance = db.Column(db.String(100))
        parking_ownership = db.Column(db.String(100))
        parking_surface = db.Column(db.String(100))
        has_cctv = db.Column(db.String(10))
        has_boom_barrier = db.Column(db.String(10))
        ticket_generated = db.Column(db.String(10))
        entry_exit_gates = db.Column(db.String(100))
        weekly_off = db.Column(db.String(50))
        parking_timing = db.Column(db.String(100))
        vehicle_types = db.Column(db.String(100))
        car_capacity = db.Column(db.Integer)
        two_wheeler_capacity = db.Column(db.Integer)
        parking_type = db.Column(db.String(100))
        payment_modes = db.Column(db.String(100))
        car_parking_charge = db.Column(db.String(100))
        two_wheeler_parking_charge = db.Column(db.String(100))
        allows_prepaid_passes = db.Column(db.String(10))
        provides_valet_services = db.Column(db.String(10))
        value_added_services = db.Column(db.Text)
        notes = db.Column(db.Text)
        total_slots = db.Column(db.Integer)
        available_slots = db.Column(db.Integer)
        address1 = db.Column(db.Float)
        address2 = db.Column(db.Float)
        two_wheeler_parking_carge = db.Column(db.Float)

    

    class Floor(db.Model):
        __tablename__ = 'floors'
        floor_id = db.Column(db.Integer, primary_key=True)
        floor_name = db.Column(db.String(50))
        rows = db.relationship('Row', backref='floor', lazy=True)
    
    

    class Row(db.Model):
        __tablename__ = 'rows'
        row_id = db.Column(db.Integer, primary_key=True)
        floor_id = db.Column(db.Integer, db.ForeignKey('floors.floor_id'))
        row_name = db.Column(db.String(50))
        slots = db.relationship('Slot', backref='row', lazy=True)

    class Slot(db.Model):
        __tablename__ = 'slots'
        slot_id = db.Column(db.Integer, primary_key=True)
        row_id = db.Column(db.Integer, db.ForeignKey('rows.row_id'))
        slot_name = db.Column(db.String(50))
        status = db.Column(db.Integer, default=1)
        vehicle_reg_no = db.Column(db.String(20), nullable=True)
        ticket_id = db.Column(db.String(20), nullable=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    class User(db.Model):
        __tablename__ = 'users'
        user_id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String(100), nullable=False)
        user_phone_no = db.Column(db.BigInteger, nullable=False)
        user_address = db.Column(db.String(255))
        user_email = db.Column(db.String(100))
        user_password = db.Column(db.String(255))

    class Reservation(db.Model):
        __tablename__ = 'reservations'
        reservation_id = db.Column(db.Integer, primary_key=True)
        slot_id = db.Column(db.Integer, db.ForeignKey('slots.slot_id'), nullable=False)
        hour = db.Column(db.Integer, nullable=False)
        reserved = db.Column(db.Boolean, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    class ParkingSession(db.Model):
        __tablename__ = 'parkingsessions'
        ticket_id = db.Column(db.String(20), primary_key=True)
        slot_id = db.Column(db.Integer, db.ForeignKey('slots.slot_id'))
        vehicle_reg_no = db.Column(db.String(20))
        start_time = db.Column(db.DateTime, default=datetime.utcnow)
        end_time = db.Column(db.DateTime, nullable=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # ROUTES


    @app.route('/')
    def home():
        return '''
        <h1>Welcome to the Car Parking System API!</h1>
        <p><a href="/parkinglots_details" style="display:inline-block;padding:10px 20px;background-color:#28a745;color:white;text-decoration:none;border-radius:5px;">View Parking Lots Details</a></p>
        <p><a href="/parking_lot" style="display:inline-block;padding:10px 20px;background-color:#007bff;color:white;text-decoration:none;border-radius:5px;">View Parking Lot Structure</a></p>
        <p><a href="/users" style="display:inline-block;padding:10px 20px;background-color:#17a2b8;color:white;text-decoration:none;border-radius:5px;">Get All Users</a></p>
        <p><strong>POST Endpoints (use tools like Postman):</strong></p>
        <ul>
            <li><code>/park_car</code> - Park a car (POST)</li>
            <li><code>/remove_car_by_ticket</code> - Remove car by ticket (DELETE)</li>
            <li><code>/users</code> - Create a new user (POST)</li>
            <li><code>/users/&lt;user_id&gt;</code> - Update user by ID (PUT)</li>
        </ul>
        <p style="color:gray;">Note: POST/PUT/DELETE endpoints need JSON input via tools like Postman or frontend integration.</p>
    '''

    # GET Endpoints
    @app.route('/parkinglots_details', methods=['GET'])
    def get_parkinglots_details():
        entries = ParkingData.query.all()
        return jsonify([
        {
            'parking_name': e.parking_name,
            'city': e.city,
            'parking_location': e.parking_location,
            'address_1': e.address_1,
            'address_2': e.address_2,
            'latitude': e.latitude,
            'longitude': e.longitude,
            'physical_appearance': e.physical_appearance,
            'parking_ownership': e.parking_ownership,
            'parking_surface': e.parking_surface,
            'has_cctv': e.has_cctv,
            'has_boom_barrier': e.has_boom_barrier,
            'ticket_generated': e.ticket_generated,
            'entry_exit_gates': e.entry_exit_gates,
            'weekly_off': e.weekly_off,
            'parking_timing': e.parking_timing,
            'vehicle_types': e.vehicle_types,
            'car_capacity': e.car_capacity,
            'two_wheeler_capacity': e.two_wheeler_capacity,
            'parking_type': e.parking_type,
            'payment_modes': e.payment_modes,
            'car_parking_charge': e.car_parking_charge,
            'two_wheeler_parking_charge': e.two_wheeler_parking_charge,
            'allows_prepaid_passes': e.allows_prepaid_passes,
            'provides_valet_services': e.provides_valet_services,
            'value_added_services': e.value_added_services,
            'notes': e.notes,
            'total_slots': e.total_slots,
            'available_slots': e.available_slots,
            'parking_id': e.parking_id
        }
        for e in entries
    ])

    @app.route('/parking_lot', methods=['GET'])
    def display_parking_lot():
        floors = Floor.query.all()
        result = []
        for floor in floors:
            floor_data = {
                'floor_id': floor.floor_id,
                'floor_name': floor.floor_name,
                'rows': []
            }
            for row in floor.rows:
                row_data = {
                    'row_id': row.row_id,
                    'row_name': row.row_name,
                    'slots': []
                }
                for slot in row.slots:
                    slot_data = {
                        'slot_id': slot.slot_id,
                        'slot_name': slot.slot_name,
                        'status': slot.status,
                        'vehicle_reg_no': slot.vehicle_reg_no,
                        'ticket_id': slot.ticket_id
                    }
                    row_data['slots'].append(slot_data)
                floor_data['rows'].append(row_data)
            result.append(floor_data)
        return jsonify(result), 200
    
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([
            {
                'user_id': user.user_id,
                'user_name': user.user_name,
                'user_email': user.user_email,
                'user_phone_no': user.user_phone_no,
                'user_address': user.user_address
            } for user in users
        ]), 200
    

    @app.route('/park_car', methods=['POST'])
    def park_car():
        data = request.get_json()
        slot_id = data.get('slot_id')
        vehicle_reg_no = data.get('vehicle_reg_no')
        user_id = data.get('user_id')
        slot = Slot.query.get(slot_id)
        if not slot or slot.status == 0:
            return jsonify({'error': 'Slot is not available'}), 400
        ticket_id = f"TKT-{slot_id}-{int(datetime.utcnow().timestamp())}"
        slot.status = 0
        slot.vehicle_reg_no = vehicle_reg_no
        slot.ticket_id = ticket_id
        slot.user_id = user_id
        session = ParkingSession(
            ticket_id=ticket_id,
            slot_id=slot_id,
            vehicle_reg_no=vehicle_reg_no,
            user_id=user_id
        )
        db.session.add(session)
        db.session.commit()
        return jsonify({'message': 'Car parked successfully', 'ticket_id': ticket_id}), 201

    @app.route('/remove_car_by_ticket', methods=['DELETE'])
    def remove_car_by_ticket():
        data = request.get_json()
        ticket_id = data.get('ticket_id')
        slot = Slot.query.filter_by(ticket_id=ticket_id).first()
        if not slot:
            return jsonify({'error': 'Ticket not found'}), 404
        session = ParkingSession.query.get(ticket_id)
        if not session:
            return jsonify({'error': 'Parking session not found'}), 404
        slot.status = 1
        slot.vehicle_reg_no = None
        slot.ticket_id = None
        slot.user_id = None
        session.end_time = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Car removed successfully'}), 200



    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_password=data['user_password'],
            user_phone_no=data['user_phone_no'],
            user_address=data['user_address']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'User with this email or phone already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        data = request.get_json()
        user.user_name = data.get('user_name', user.user_name)
        user.user_email = data.get('user_email', user.user_email)
        user.user_password = data.get('user_password', user.user_password)
        user.user_phone_no = data.get('user_phone_no', user.user_phone_no)
        user.user_address = data.get('user_address', user.user_address)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()



    return app
