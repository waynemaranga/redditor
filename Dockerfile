FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY src/ src/
COPY requirements.txt ./
COPY README.md ./
RUN mkdir -p logs/
RUN pip install -r requirements.txt --no-cache-dir --quiet
RUN pip install -e .

EXPOSE 8045

# Command to run the FastAPI app with uvicorn
CMD ["python", "-m", "uvicorn", "redditor.server.server:app", "--host", "0.0.0.0", "--port", "8045", "--reload"]
