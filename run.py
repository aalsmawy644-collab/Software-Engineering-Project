import os
import socket
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription, PrescriptionItem

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db, User=User, Role=Role,
        Doctor=Doctor, Patient=Patient,
        Appointment=Appointment,
        MedicalRecord=MedicalRecord,
        Prescription=Prescription,
        PrescriptionItem=PrescriptionItem
    )


def find_available_port(start_port=5000, candidate_ports=(5000, 5050, 8000, 8080, 5500)):
    """Find the first available open port to avoid socket permission / conflict errors on Windows."""
    env_port = os.environ.get('PORT')
    if env_port:
        return int(env_port)

    for port in candidate_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return start_port


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("[OK] Database verified.")

    port = find_available_port(5050)
    print("\n" + "=" * 55)
    print("  CLINIC MANAGEMENT SYSTEM SERVER RUNNING")
    print("=" * 55)
    print(f"  Access URL: http://127.0.0.1:{port}")
    print(f"  Localhost:  http://localhost:{port}")
    print("=" * 55 + "\n")

    app.run(debug=True, host='127.0.0.1', port=port)
