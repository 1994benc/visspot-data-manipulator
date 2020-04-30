# visspot-data-manipulator
A backend service to manipulate data for VisSpot.com

## Run the service locally
Start a virtual environment
````python
python3 -m venv env
source env/bin/activate
````
Install dependencies
````python 
pip install -r requirements.txt
````
Download [Google private key](https://firebase.google.com/docs/admin/setup#initialize-sdk "Google private key") in a json file and put it in a folder named `rainbow` in the app level directory.

In `admin.py` add the path to your Google private key
```python
cred = credentials.Certificate(
    "rainbow/<YOUR_PRIVATE_KEY>.json")
```
Run the server locally
```python
python app.py
```
The server will start on port 0.0.0.0
