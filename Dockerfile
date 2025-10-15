FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# expose ports: 8000 FastAPI, 8001 MCP
EXPOSE 8000
EXPOSE 8001

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & python mcp_server.py"]
