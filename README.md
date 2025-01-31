## Simple API and tg bot for checking device by IMEI.
Stack: Python, FastAPI, aiogram, SQLAlchemy, Alembic

# Bot Commands
- `/start`

# Run
```python
python -m venv venv
pip install -r requirements.txt
alembic upgrade head
```

```python
python run.py
```
# About

#### API Docs - ```http://0.0.0.0:8000/docs``` 
#### Register ```http://0.0.0.0:8000/auth/register``` 
#### -> Login ```http://0.0.0.0:8000/auth/login``` 
#### -> Get API Token ```http://0.0.0.0:8000/api/get_token```
#### Also u can use API Token from env to send API requests 
#### Add users to whitelist ```http://0.0.0.0:8000/api/add-user-to-whitelist``` 
#### Send request to imeicheck ```http://0.0.0.0:8000/api/check-imei```

