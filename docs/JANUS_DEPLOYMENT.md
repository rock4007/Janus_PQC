# Janus Deployment

## GitHub
- Add `minor-projects/Janus_PQC_README.md` to your repo README index.
- Include `minor-projects/docs/` in documentation for overview and security.

## Local
```powershell
python c:\Users\User\Documents\minor-projects\Janus_PQC
```

## Docker
```bash
docker build -t janus-pqc c:\Users\User\Documents\minor-projects
docker run --rm janus-pqc
```

## WSL/Linux with oqs
- Install `python-oqs` per official guide.
- No code changes required; adapter switches to oqs automatically.
