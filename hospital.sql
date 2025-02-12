-- Create Patients Table
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

-- Create Doctors Table
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100)
);

-- Create Schedules Table
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    doctor_id INTEGER NOT NULL,
    schedule_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Sample Initial Data for Doctors
INSERT INTO doctors (first_name, last_name, specialization) VALUES 
('John', 'Smith', 'Cardiology'),
('Emily', 'Johnson', 'Pediatrics'),
('Michael', 'Williams', 'Neurology');