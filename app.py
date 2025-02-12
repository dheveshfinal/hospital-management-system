from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/hospital_management_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100))

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    schedule_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    doctor = db.relationship('Doctor', backref=db.backref('schedules', lazy=True))

# Root route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    new_patient = Patient(
        first_name=data['firstName'],
        last_name=data['lastName'],
        birth_date=datetime.strptime(data['birthDate'], '%Y-%m-%d').date(),
        gender=data['gender'],
        contact_number=data['contactNumber'],
        email=data['email']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient created', 'id': new_patient.id}), 201

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    patient_list = [{
        'id': patient.id,
        'firstName': patient.first_name,
        'lastName': patient.last_name,
        'birthDate': patient.birth_date.isoformat(),
        'gender': patient.gender,
        'contactNumber': patient.contact_number,
        'email': patient.email
    } for patient in patients]
    return jsonify(patient_list)

@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    data = request.json
    new_schedule = Schedule(
        doctor_id=data['doctorId'],
        schedule_date=datetime.strptime(data['scheduleDate'], '%Y-%m-%d').date(),
        start_time=datetime.strptime(data['startTime'], '%H:%M').time(),
        end_time=datetime.strptime(data['endTime'], '%H:%M').time()
    )
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule created', 'id': new_schedule.id}), 201

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    schedules = Schedule.query.all()
    schedule_list = [{
        'id': schedule.id,
        'doctorId': schedule.doctor_id,
        'doctorName': f"{schedule.doctor.first_name} {schedule.doctor.last_name}",
        'scheduleDate': schedule.schedule_date.isoformat(),
        'startTime': schedule.start_time.strftime('%H:%M'),
        'endTime': schedule.end_time.strftime('%H:%M')
    } for schedule in schedules]
    return jsonify(schedule_list)

def init_db():
    with app.app_context():
        db.create_all()
        # Create some initial doctors if not exists
        if not Doctor.query.first():
            doctors = [
                Doctor(first_name='John', last_name='Smith', specialization='Cardiology'),
                Doctor(first_name='Emily', last_name='Johnson', specialization='Pediatrics'),
                Doctor(first_name='Michael', last_name='Williams', specialization='Neurology')
            ]
            db.session.add_all(doctors)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)