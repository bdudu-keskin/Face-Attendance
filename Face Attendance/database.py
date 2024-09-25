import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-67f39-default-rtdb.firebaseio.com/"
})

ref = db.reference('students')

data = {
    "321654": {
        "name": "murtaza hasan",
        "major": "robotics",
        "starting year": 2017,
        "total attendance": 6,
        "standing": "G",
        "year": 4,
        "last attendance": "2022-12-11 00:54:34"
    },

    "852741": {
        "name": "emily blunt",
        "major": "economics",
        "starting year": 2021,
        "total attendance": 12,
        "standing": "B",
        "year": 2,
        "last attendance": "2022-12-11 00:54:34"
    },

    "963852": {
        "name": "elon musk",
        "major": "physics",
        "starting year": 2020,
        "total attendance": 7,
        "standing": "G",
        "year": 2,
        "last attendance": "2022-12-11 00:54:34"
    },

    "101127": {
        "name": "dudu keskin",
        "major": "engineering",
        "starting year": 2022,
        "total attendance": 14,
        "standing": "B",
        "year": 3,
        "last attendance": "2022-12-11 00:54:34"
    },

    "101930": {
        "name": "ebru karabürk",
        "major": "engineering",
        "starting year": 2021,
        "total attendance": 14,
        "standing": "B",
        "year": 3,
        "last attendance": "2022-12-11 00:54:34"
    }
}

for key, value in data.items():
    ref.child(key).set(value)