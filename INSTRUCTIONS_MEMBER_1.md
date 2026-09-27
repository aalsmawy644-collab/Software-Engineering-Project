<div dir="rtl">

# 📋 دليل إرشادات العضو الأول (Member 1)
### دورك: مهندس البنية التحتية والمسؤول عن النواة ونظام الإدارة (Core & Admin Lead)

مرحباً بك! يحتوي هذا المجلد على النصف الأول من المشروع. مهمتك هي إنشاء مستودع المشروع (Repository) على GitHub ورفع هذا الأساس، ثم دعوة زميلك في الفريق.

---

### 📂 محتويات مجلدك:
1. **ملفات الإعداد والنواة:** `run.py`, `config.py`, `requirements.txt`, `.gitignore`, `README.md`.
2. **التصميم العام:** مجلد `app/static/` والقالب الأساسي `app/templates/base.html`.
3. **نماذج البيانات:** `models/user.py`, `models/doctor.py`, `models/patient.py`.
4. **المسارات والواجهات:** نظام تسجيل الدخول والمصادقة (`auth`) ولوحة تحكم المسؤول وإدارة الحسابات (`admin`).

---

### 🚀 خطوات الرفع خطوة بخطوة:

#### 1. افتح موجه الأوامر (Terminal / PowerShell) داخل هذا المجلد:
تأكد أنك داخل مجلد `Member_1_Project`.

#### 2. تهيئة Git وإضافة الملفات:
نفّذ الأوامر التالية بالترتيب:
```bash
git init
git add .
git commit -m "feat: Initial setup, core architecture, auth and admin portal"
```

#### 3. إنشاء المستودع على GitHub:
- توجه إلى موقع [GitHub.com](https://github.com) وسجل دخولك.
- اضغط على **New Repository**.
- سمّ المستودع باسم المشروع (مثلاً: `ClinicMS` أو `clinic-management-system`).
- اجعل المستودع **Public** أو **Private** حسب رغبتك.
- **تنبيه:** لا تضع علامة صح على "Add a README file" لأن لديك بالفعل ملف README جاهز.
- اضغط **Create repository**.

#### 4. ربط المستودع ورفع الكود:
انسخ رابط المستودع الخاص بك واستبدل الرابط في الأمر التالي:
```bash
git branch -M main
git remote add origin https://github.com/اسم_حسابك/اسم_المستودع.git
git push -u origin main
```

#### 5. دعوة العضو الثاني (زميلك):
- من صفحة المستودع على GitHub، اضغط على **Settings**.
- من القائمة الجانبية اختر **Collaborators**.
- اضغط على **Add people**.
- اكتب اسم مستخدم زميلك على GitHub أو بريده الإلكتروني وأرسل له الدعوة.

---
✨ **انتهت مهمتك الأولى بنجاح! الآن أخبر العضو الثاني ليبدأ عمله.**
</div>
