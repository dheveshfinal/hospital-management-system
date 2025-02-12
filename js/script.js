document.getElementById('patientForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const patient = {
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        birthDate: document.getElementById('birthDate').value,
        gender: document.getElementById('gender').value,
        contactNumber: document.getElementById('contactNumber').value,
        email: document.getElementById('email').value
    };

    fetch('/api/patients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(patient)
    })
    .then(response => response.json())
    .then(data => {
        alert('Patient Registered Successfully');
        loadPatients();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Registration Failed');
    });
});

document.getElementById('scheduleForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const schedule = {
        doctorId: document.getElementById('doctorSelect').value,
        scheduleDate: document.getElementById('scheduleDate').value,
        startTime: document.getElementById('startTime').value,
        endTime: document.getElementById('endTime').value
    };

    fetch('/api/schedules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(schedule)
    })
    .then(response => response.json())
    .then(data => {
        alert('Schedule Created Successfully');
        loadSchedules();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Schedule Creation Failed');
    });
});

function loadPatients() {
    fetch('/api/patients')
        .then(response => response.json())
        .then(patients => {
            const tableBody = document.getElementById('patientTableBody');
            tableBody.innerHTML = '';
            patients.forEach(patient => {
                const row = `
                    <tr>
                        <td>${patient.id}</td>
                        <td>${patient.firstName} ${patient.lastName}</td>
                        <td>${patient.birthDate}</td>
                        <td>${patient.gender}</td>
                        <td>${patient.contactNumber}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        });
}

function loadSchedules() {
    fetch('/api/schedules')
        .then(response => response.json())
        .then(schedules => {
            const tableBody = document.getElementById('scheduleTableBody');
            tableBody.innerHTML = '';
            schedules.forEach(schedule => {
                const row = `
                    <tr>
                        <td>Dr. ${schedule.doctorName}</td>
                        <td>${schedule.scheduleDate}</td>
                        <td>${schedule.startTime}</td>
                        <td>${schedule.endTime}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        });
}

// Load data on page load
loadPatients();
loadSchedules();