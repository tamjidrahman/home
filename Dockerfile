FROM python:3.12-slim

WORKDIR /app

# Install dependencies directly with pip (simpler, faster builds)
COPY pyproject.toml ./
RUN pip install --no-cache-dir toml && \
    python -c "import toml; c=toml.load('pyproject.toml'); print('\n'.join(f'{k}{v}' for k,v in c['tool']['poetry']['dependencies'].items() if k!='python'))" > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY homeassistant/ ./homeassistant/
COPY api.py config.toml ./

# Set config path to use bundled config
ENV HOME_CONFIG_PATH=/app/config.toml

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
