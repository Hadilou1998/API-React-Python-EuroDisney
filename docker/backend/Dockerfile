FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    sqlalchemy \
    pymysql \
    pydantic \
    pydantic-settings \
    "python-jose[cryptography]" \
    passlib==1.7.4 \
    bcrypt==4.0.1 \
    python-multipart \
    qrcode \
    pillow

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]