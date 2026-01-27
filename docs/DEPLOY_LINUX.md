# Deploy on Linux

This guide shows how to run Janus_PQC on Linux servers via Python, Docker, and systemd.

## Prerequisites
- Linux (Ubuntu/Debian/CentOS/Alma, etc.)
- Python 3.11+
- Optional: Docker / Kubernetes

## Run with Python
```bash
# Clone or copy the repo
cd janus-pqc
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run main script
python Janus_PQC

# Run tests
python run_tests_janus_pqc.py
```

## Systemd Service
Create a unit file to run on boot.

1) Path layout (example):
- Repo: /opt/janus-pqc
- Python: /usr/bin/python3

2) Unit file: /etc/systemd/system/janus-pqc.service
```
[Unit]
Description=Janus_PQC Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/janus-pqc
ExecStart=/usr/bin/python3 /opt/janus-pqc/Janus_PQC
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

3) Enable + start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable janus-pqc
sudo systemctl start janus-pqc
sudo systemctl status janus-pqc
```

## Docker
```bash
# Build
docker build -t janus-pqc:latest .

# Run
docker run --rm janus-pqc:latest
```

## Kubernetes (Optional)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: janus-pqc
spec:
  replicas: 1
  selector:
    matchLabels: { app: janus-pqc }
  template:
    metadata:
      labels: { app: janus-pqc }
    spec:
      containers:
        - name: janus-pqc
          image: <REGISTRY_PATH>/janus-pqc:latest
          imagePullPolicy: Always
```

## Security & Compliance Notes
- For regulated/government use, operate with FIPS 140-3 validated crypto modules and FIPS mode where applicable.
- Store keys in HSM/KMS; enforce RBAC, logging, audit trails.
- Track SBOM and run dependency audits (pip-audit) continuously.
