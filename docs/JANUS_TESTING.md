# Janus Testing

## Black-Box
- `tests/test_black_box_janus_pqc.py` runs random-message verification and tamper detection.
- `run_tests_janus_pqc.py` is a convenience runner.

## Commands
```powershell
python c:\Users\User\Documents\minor-projects\run_tests_janus_pqc.py
```

## Expected
- All random messages verify successfully.
- Tampered message fails verification.
