# Run Instructions

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 validate_data.py
python3 -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python validate_data.py
python -m streamlit run app.py
```
