# بوت وعد — نسخة الإصلاح

## المتطلبات

- Python 3.11 أو 3.12
- Redis
- FFmpeg
- توكن جديد من BotFather؛ لا تستخدم التوكن الموجود في النسخة القديمة

## التثبيت

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

انسخ أسماء الإعدادات من `.env.example` إلى بيئة تشغيل آمنة. لا تضع القيم الحقيقية داخل ملفات المشروع ولا ترسلها في المحادثات.

## الإعدادات الإلزامية

```text
BOT_TOKEN
API_ID
API_HASH
OWNER_ID
```

الإعدادات الاختيارية:

```text
REDIS_URL
BOT_USERNAME
DATA_DIR
LOG_LEVEL
ARQ_API_KEY
ARQ_API_URL
```

## التشغيل

بعد تصدير متغيرات البيئة:

```bash
chmod +x start.sh
./start.sh
```

أو مباشرة:

```bash
python3 main.py
```

## الفحص

```bash
python3 -m compileall -q .
python3 -m unittest discover -s tests -v
```

## ملاحظات أمنية

- أوامر تنفيذ Python وShell عن بعد محذوفة.
- تعديل ملفات البوت من Telegram محذوف.
- تغيير المالك يتم عبر `OWNER_ID` في بيئة التشغيل فقط.
- لا تُضف ملفات `.env` أو الجلسات أو قواعد البيانات إلى Git.
