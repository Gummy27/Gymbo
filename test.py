import pyodbc
import json

conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
                      'Server=gummi-B450M-DS3H;'
                      'Database=GYMBO;'
                      "UID=SA;"
                      "PWD=Aegishjalmur27;" 
                      "Trusted_Connection=no;"
                      )

cursor = conn.cursor()
cursor.execute("select * from exercises")

for i in cursor:
    print(i)

class Data_handler:
    def __init__(self) -> None:
        self.exercise_keys = self.get_exercise_keys()
        print(self.exercise_keys)
    
    def get_exercise_keys(self):
        exercise_keys = {}

        try:
            with open("static/exercise_keys.json", 'r') as file:
                file_json = json.load(file)
                for index, exercise in enumerate(file_json["exercises"]):
                    exercise_keys[index] = exercise
        except FileNotFoundError as err:
            print(f"Data handler has crashed: {err}")
            raise

        return exercise_keys

    



Data_handler()


                    