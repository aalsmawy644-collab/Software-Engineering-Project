"""
زراعة وتوليد بيانات عربية واقعية وشاملة لنظام إدارة العيادة الطبية.
Arabic Database Seeding Script for Clinic Management System.
Run: python seed.py
"""
import os
import sys
from datetime import date, time, timedelta

# Fix Windows console encoding for Arabic text output
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription, PrescriptionItem


def seed_database():
    app = create_app('development')
    with app.app_context():
        print("جاري حذف وإعادة إنشاء جميع الجداول في قاعدة البيانات...")
        db.drop_all()
        db.create_all()
        print("[OK] تم إنشاء الجداول بنجاح.\n")

        # ── الأدوار والصلاحيات (Roles) ──────────────────────────
        admin_role = Role(name='admin', description='مدير النظام (System Administrator)')
        doctor_role = Role(name='doctor', description='طبيب معالج (Medical Doctor)')
        patient_role = Role(name='patient', description='مريض مراجع (Patient)')
        db.session.add_all([admin_role, doctor_role, patient_role])
        db.session.commit()
        print("[OK] تم إنشاء الأدوار (مدير، طبيب، مريض).")

        # ── مدير النظام (Admin) ──────────────────────────────────
        admin_user = User(
            username='admin',
            email='admin@clinic.com',
            first_name='عبدالرحمن',
            last_name='السعيد',
            phone='0501112233',
            role_id=admin_role.id
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)

        # ── الكادر الطبي والأطباء (Doctors) ─────────────────────
        # 1. د. أحمد الغامدي (باطنية وطب عام)
        d1_user = User(
            username='dr.ahmed',
            email='ahmed@clinic.com',
            first_name='أحمد',
            last_name='الغامدي',
            phone='0505551101',
            role_id=doctor_role.id
        )
        d1_user.set_password('doctor123')

        # 2. د. سارة المطيري (أمراض قلب)
        d2_user = User(
            username='dr.sarah',
            email='sarah@clinic.com',
            first_name='سارة',
            last_name='المطيري',
            phone='0505551102',
            role_id=doctor_role.id
        )
        d2_user.set_password('doctor123')

        # 3. د. خالد الشمري (جلدية وتجميل)
        d3_user = User(
            username='dr.khalid',
            email='khalid@clinic.com',
            first_name='خالد',
            last_name='الشمري',
            phone='0505551103',
            role_id=doctor_role.id
        )
        d3_user.set_password('doctor123')

        db.session.add_all([d1_user, d2_user, d3_user])
        db.session.flush()

        doctor1 = Doctor(
            user_id=d1_user.id,
            specialty='طب عام وباطنية (General Medicine)',
            license_number='LIC-SA-101',
            experience_years=12,
            consultation_fee=150.0,
            working_start_time=time(8, 0),
            working_end_time=time(16, 0),
            bio='استشاري الطب الباطني والأسرة بخبرة 12 عاماً، متخصص في تشخيص وعلاج الأمراض المزمنة والفحص الوقائي الدوري.'
        )
        doctor2 = Doctor(
            user_id=d2_user.id,
            specialty='أمراض القلب (Cardiology)',
            license_number='LIC-SA-102',
            experience_years=15,
            consultation_fee=250.0,
            working_start_time=time(9, 0),
            working_end_time=time(17, 0),
            bio='استشارية أمراض القلب والقسطرة، حاصلة على البورد في تصوير القلب وتخطيط الجهد والوقاية من الجلطات.'
        )
        doctor3 = Doctor(
            user_id=d3_user.id,
            specialty='جلدية وتجميل (Dermatology)',
            license_number='LIC-SA-103',
            experience_years=9,
            consultation_fee=180.0,
            working_start_time=time(13, 0),
            working_end_time=time(21, 0),
            bio='أخصائي أول في الأمراض الجلدية وعلاج الحساسية الجلدية المزمنة والإكزيما وحب الشباب والعلاج بالليزر.'
        )
        db.session.add_all([doctor1, doctor2, doctor3])

        # ── المرضى (Patients) ────────────────────────────────────
        # 1. محمد بن علي العتيبي
        p1_user = User(
            username='mohammed.ali',
            email='mohammed@email.com',
            first_name='محمد',
            last_name='العتيبي',
            phone='0551234567',
            role_id=patient_role.id
        )
        p1_user.set_password('patient123')

        # 2. فاطمة الزهراء الشريف
        p2_user = User(
            username='fatima.z',
            email='fatima@email.com',
            first_name='فاطمة',
            last_name='الشريف',
            phone='0509876543',
            role_id=patient_role.id
        )
        p2_user.set_password('patient123')

        # 3. عبدالله بن خالد الدوسري
        p3_user = User(
            username='abdullah.k',
            email='abdullah@email.com',
            first_name='عبدالله',
            last_name='الدوسري',
            phone='0543322110',
            role_id=patient_role.id
        )
        p3_user.set_password('patient123')

        # 4. نورة بنت سعد القحطاني
        p4_user = User(
            username='noura.saad',
            email='noura@email.com',
            first_name='نورة',
            last_name='القحطاني',
            phone='0567788990',
            role_id=patient_role.id
        )
        p4_user.set_password('patient123')

        db.session.add_all([p1_user, p2_user, p3_user, p4_user])
        db.session.flush()

        patient1 = Patient(
            user_id=p1_user.id,
            date_of_birth=date(1986, 4, 15),
            gender='Male',
            blood_type='O+',
            address='الرياض - حي النرجس - شارع التخصصي',
            emergency_contact='علي العتيبي (الوالد)',
            emergency_phone='0551110000',
            allergies='حساسية بنسلين',
            chronic_conditions='ارتفاع ضغط الدم الخفيف',
            insurance_number='INS-SA-1001'
        )
        patient2 = Patient(
            user_id=p2_user.id,
            date_of_birth=date(1992, 9, 20),
            gender='Female',
            blood_type='A-',
            address='جدة - حي الروضة - طريق الكورنيش',
            emergency_contact='طارق الشريف (الزوج)',
            emergency_phone='0502220000',
            allergies='لا يوجد',
            chronic_conditions='خفقان وإجهاد عرضي',
            insurance_number='INS-SA-1002'
        )
        patient3 = Patient(
            user_id=p3_user.id,
            date_of_birth=date(1979, 11, 12),
            gender='Male',
            blood_type='B+',
            address='الدمام - حي الشاطئ',
            emergency_contact='سعود الدوسري (الأخ)',
            emergency_phone='0543330000',
            allergies='مركبات السلفا، أسبرين',
            chronic_conditions='السكري من النوع الثاني، ضغط الدم',
            insurance_number='INS-SA-1003'
        )
        patient4 = Patient(
            user_id=p4_user.id,
            date_of_birth=date(1996, 3, 8),
            gender='Female',
            blood_type='AB+',
            address='الخبر - حي الحزام الذهبي',
            emergency_contact='سعد القحطاني (الوالد)',
            emergency_phone='0564440000',
            allergies='لاتكس',
            chronic_conditions='حساسية جلدية وربو موسمي خفيف',
            insurance_number='INS-SA-1004'
        )
        db.session.add_all([patient1, patient2, patient3, patient4])
        db.session.commit()
        print("[OK] تم إنشاء حسابات الأطباء والمرضى بالعربية.")

        # ── المواعيد والكشوفات (Appointments) ───────────────────
        today = date.today()
        appointments = [
            Appointment(patient_id=patient1.id, doctor_id=doctor1.id,
                        appointment_date=today - timedelta(days=5),
                        appointment_time=time(9, 0), status='Completed',
                        reason='فحص سنوي ومتابعة قياسات ضغط الدم والصداع', duration_minutes=30),
            Appointment(patient_id=patient2.id, doctor_id=doctor2.id,
                        appointment_date=today - timedelta(days=2),
                        appointment_time=time(10, 30), status='Completed',
                        reason='استشارة تخطيط قلب وفحص ألم الصدر مع الإجهاد', duration_minutes=45),
            Appointment(patient_id=patient4.id, doctor_id=doctor3.id,
                        appointment_date=today - timedelta(days=8),
                        appointment_time=time(16, 0), status='Completed',
                        reason='فحص طفح وحكة جلدية في الذراعين', duration_minutes=30),
            Appointment(patient_id=patient3.id, doctor_id=doctor1.id,
                        appointment_date=today + timedelta(days=1),
                        appointment_time=time(11, 0), status='Scheduled',
                        reason='متابعة معدلات السكر التراكمي وتحاليل الكلى', duration_minutes=30),
            Appointment(patient_id=patient1.id, doctor_id=doctor1.id,
                        appointment_date=today + timedelta(days=3),
                        appointment_time=time(14, 30), status='Scheduled',
                        reason='مراجعة قراءات الضغط المنزلية', duration_minutes=20),
            Appointment(patient_id=patient2.id, doctor_id=doctor2.id,
                        appointment_date=today + timedelta(days=7),
                        appointment_time=time(9, 30), status='Scheduled',
                        reason='متابعة نتائج تصوير الإيكو القلبي', duration_minutes=45),
        ]
        db.session.add_all(appointments)
        db.session.commit()
        appt1, appt2, appt3, appt4, appt5, appt6 = appointments
        print("[OK] تم إنشاء المواعيد والحجوزات.")

        # ── السجلات والتقارير الطبية (Medical Records) ──────────
        record1 = MedicalRecord(
            patient_id=patient1.id,
            doctor_id=doctor1.id,
            appointment_id=appt1.id,
            visit_date=today - timedelta(days=5),
            chief_complaint='صداع متكرر خفيف في مؤخرة الرأس مع فحص روتيني شامل.',
            diagnosis='ارتفاع ضغط دم أولي تحت السيطرة. المؤشرات الحيوية مستقرة والفحص السريري سليم.',
            treatment_plan='الاستمرار على دواء أملوديبين 5 ملجم، اتباع حمية قليلة الصوديوم، والمشي 30 دقيقة يومياً.',
            notes='الضغط: 126/80 ملم زئبق، النبض: 72 ن/د، الوزن: 78 كجم، فحص قاع العين سليم.',
            follow_up_date=today + timedelta(days=90)
        )
        record2 = MedicalRecord(
            patient_id=patient2.id,
            doctor_id=doctor2.id,
            appointment_id=appt2.id,
            visit_date=today - timedelta(days=2),
            chief_complaint='ألم ضاغط في منتصف الصدر يزداد مع المجهود البدني والتوتر منذ 4 أيام.',
            diagnosis='ذبحة صدرية مستقرة ناتجة عن الإجهاد. تم استبعاد أي احتشاء حاد في عضلة القلب.',
            treatment_plan='نيتروجلسرين تحت اللسان عند اللزوم، راحة تامة، حمية البحر الأبيض المتوسط، وعمل إيكو وتخطيط جهد.',
            notes='تخطيط القلب (EKG) سليم، إنزيمات القلب (تروبونين) سالبة x2، الضغط: 132/84.',
            follow_up_date=today + timedelta(days=14)
        )
        record3 = MedicalRecord(
            patient_id=patient4.id,
            doctor_id=doctor3.id,
            appointment_id=appt3.id,
            visit_date=today - timedelta(days=8),
            chief_complaint='طفح جلدي أحمر مع حكة شديدة في الساعدين والبطن منذ أسبوع.',
            diagnosis='التهاب جلد تحسسي تماسي (Allergic Contact Dermatitis) ناتج عن منظف جديد.',
            treatment_plan='كريم هيدروكورتيزون موضعي مرتين يومياً، مضاد هيستامين قبل النوم، وتجنب ملامسة المادة المحسسة.',
            notes='الطفح منتشر في الساعدين بدون علامات عدوى بكتيرية ثانوية.',
            follow_up_date=today + timedelta(days=15)
        )
        db.session.add_all([record1, record2, record3])
        db.session.commit()
        print("[OK] تم إنشاء التقارير الطبية السريرية.")

        # ── الوصفات العلاجية والروشتات (Prescriptions) ─────────
        rx1 = Prescription(
            patient_id=patient1.id,
            doctor_id=doctor1.id,
            medical_record_id=record1.id,
            prescription_date=today - timedelta(days=5),
            instructions='تناول الأدوية بعد الأكل بانتظام، قياس ضغط الدم وتسجيله يومياً في الصباح.'
        )
        db.session.add(rx1)
        db.session.flush()
        db.session.add_all([
            PrescriptionItem(prescription_id=rx1.id, medicine_name='Amlodipine (أملوديبين)',
                             dosage='5 ملجم', frequency='مرة واحدة يومياً', duration='90 يوماً',
                             instructions='تؤخذ صباحاً بعد الإفطار'),
            PrescriptionItem(prescription_id=rx1.id, medicine_name='Lisinopril (ليزينوبريل)',
                             dosage='10 ملجم', frequency='مرة واحدة يومياً', duration='90 يوماً',
                             instructions='تؤخذ مساءً مع شرب كمية كافية من الماء'),
            PrescriptionItem(prescription_id=rx1.id, medicine_name='Aspirin Protect (أسبرين وقائي)',
                             dosage='81 ملجم', frequency='مرة واحدة يومياً', duration='مستمر',
                             instructions='تؤخذ بعد وجبة الغداء مباشرة'),
        ])

        rx2 = Prescription(
            patient_id=patient2.id,
            doctor_id=doctor2.id,
            medical_record_id=record2.id,
            prescription_date=today - timedelta(days=2),
            instructions='الالتزام التام بالراحة وتجنب رفع الأوزان الثقيلة. التوجه للطوارئ إذا استمر ألم الصدر أكثر من 15 دقيقة.'
        )
        db.session.add(rx2)
        db.session.flush()
        db.session.add_all([
            PrescriptionItem(prescription_id=rx2.id, medicine_name='Nitroglycerin (نيتروجلسرين تحت اللسان)',
                             dosage='0.4 ملجم', frequency='عند اللزوم (عند حدوث ألم الصدر)',
                             duration='30 يوماً',
                             instructions='حبة واحدة تحت اللسان عند الشعور بالألم، تكرر بعد 5 دقائق إذا لزم'),
            PrescriptionItem(prescription_id=rx2.id, medicine_name='Metoprolol (ميتوبرولول منظم نبضات)',
                             dosage='25 ملجم', frequency='مرتين يومياً',
                             duration='30 يوماً', instructions='صباحاً ومساءً بانتظام'),
        ])

        rx3 = Prescription(
            patient_id=patient4.id,
            doctor_id=doctor3.id,
            medical_record_id=record3.id,
            prescription_date=today - timedelta(days=8),
            instructions='دهان الكريم على الأماكن المصابة فقط، تجنب الصابون المعطر واستخدام مرطبات طبية.'
        )
        db.session.add(rx3)
        db.session.flush()
        db.session.add_all([
            PrescriptionItem(prescription_id=rx3.id, medicine_name='Hydrocortisone Cream 1% (كريم هيدروكورتيزون)',
                             dosage='طبقة رقيقة', frequency='مرتين يومياً',
                             duration='14 يوماً', instructions='دهان موضعي على الطفح الجلدي'),
            PrescriptionItem(prescription_id=rx3.id, medicine_name='Cetirizine (سيتريزين مضاد حساسية)',
                             dosage='10 ملجم', frequency='حبة واحدة يومياً',
                             duration='10 أيام', instructions='تؤخذ قبل النوم (قد تسبب النعاس)'),
        ])

        db.session.commit()
        print("[OK] تم إنشاء الوصفات العلاجية وقوائم الأدوية.")

        print("\n" + "=" * 60)
        print("  تمت زراعة وتوليد البيانات العربية بنجاح في قاعدة البيانات")
        print("=" * 60)
        print("\n  بيانات تسجيل الدخول التجريبية (Demo Accounts):")
        print("  +-----------------+-------------------+-------------------+")
        print("  | الدور (Role)    | اسم المستخدم      | كلمة المرور       |")
        print("  +-----------------+-------------------+-------------------+")
        print("  | مدير النظام     | admin             | admin123          |")
        print("  | طبيب باطنية     | dr.ahmed          | doctor123         |")
        print("  | طبيبة قلب       | dr.sarah          | doctor123         |")
        print("  | طبيب جلدية      | dr.khalid         | doctor123         |")
        print("  | مريض            | mohammed.ali      | patient123        |")
        print("  | مريضة           | fatima.z          | patient123        |")
        print("  | مريض            | abdullah.k        | patient123        |")
        print("  | مريضة           | noura.saad        | patient123        |")
        print("  +-----------------+-------------------+-------------------+")
        print("\n  لتشغيل الخادم: python run.py")
        print("  رابط الموقع: http://localhost:5050")
        print("=" * 60 + "\n")


if __name__ == '__main__':
    seed_database()
