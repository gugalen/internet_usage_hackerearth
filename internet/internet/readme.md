## Setup
Note: I'm using Python 3.9.1
- Create virtual environment
- Note: Ensure you have current project copied at your path
- Install dependencies using requirement.txt
```
pip install -r requirement.txt
```
- Install postgres(version 14) and start running postgres server locally
- Export below env variable in your shell which has postgres config and modify the values within "{}" as per your DB setup
```
export DATABASE_URL=postgres://{USERNAME}:{PASSWORD}@127.0.0.1:{PORT}/{DATABASE}
```
## Run Migration
```
python manage.py migrate
```
## Run Server
To run Django server locally, run below command:
```
python manage.py runserver
```
This will start Django server running on port 8000.