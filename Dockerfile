FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOST=0.0.0.0 \
    APP_PORT=7860

WORKDIR /app

# Create non-root user expected by Hugging Face Spaces
RUN useradd -m -u 1000 user

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml README.md ./
COPY configs ./configs
COPY src ./src

RUN pip install --no-cache-dir --no-deps . && chown -R user:user /app

USER user

EXPOSE 7860

CMD ["python", "-m", "cloud_smash.api.app"]
