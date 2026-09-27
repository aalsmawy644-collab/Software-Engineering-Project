from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.doctor import doctor_bp
    from app.routes.patient import patient_bp
    from app.routes.appointment import appointment_bp
    from app.routes.medical_record import medical_record_bp
    from app.routes.prescription import prescription_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(appointment_bp, url_prefix='/appointments')
    app.register_blueprint(medical_record_bp, url_prefix='/medical-records')
    app.register_blueprint(prescription_bp, url_prefix='/prescriptions')

    return app
