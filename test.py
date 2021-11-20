import pyodbc
from new_workout import New_workout
from datetime import date, datetime

class Data_handler:
    def __init__(self) -> None:
        self.__conn = pyodbc.connect('Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
                      'Server=gummi-B450M-DS3H;'
                      'Database=GYMBO;'
                      "UID=SA;"
                      "PWD=Aegishjalmur27;" 
                      "Trusted_Connection=no;"
                      )

        self.__cursor = self.__conn.cursor()
    # ------------------- Misc. methods -------------------
    def exercise_to_index(self, exercise: str) -> str:
        '''
            This function converts the exercise string into id 
            which is used in the sql database to save space.
        '''
        sql_command = f"select id from exercise_keys where exercise='{exercise}'"
        
        self.__cursor.execute(sql_command)
        
        # The program throws a index error when it didn't find anything.
        try:
            id = list(self.__cursor)[0][0]
            return id
        except IndexError:
            return None

    # ------------------- Write methods -------------------
    def add(self, new_workout: New_workout) -> None:
        '''
            This function will add the entries in the new workout object
            to the sql database
        '''
        date, sets = new_workout.into_dict()

        sql_command = "insert into exercises(day, exercise, sets) Values"
        for exercise in sets:
            formatted_set = ' '.join(sets[exercise])
            sql_command += f" ('{date}', {int(exercise)}, '{formatted_set}'),"

        self.__cursor.execute(sql_command[:-1]+";")
        self.__conn.commit()
    
    def new_personal_best(self, exercise: str, set: str, empty_pb=False) -> None:
        '''
            This function will write the new personal best to the 
            sql database.
        '''
        id = self.exercise_to_index(exercise)

        if empty_pb:
            sql_command = f"insert into personal_best(id, record) values({id}, {set});"
        else:
            sql_command = f"update personal_best set record='{set}' where id = {id};"

        self.__cursor.execute(sql_command)
        self.__conn.commit()


    # ------------------- Read methods -------------------
    def get_list_of_exercises(self) -> list:
        ''' 
            This function will return a list of exercises.
        '''
        self.__cursor.execute("select exercise from exercise_keys;")

        return [x[0] for x in self.__cursor]


    def find_prev_workout(self, exercise: str) -> list:
        '''
            This function will find the previous instance when the user
            did this exercise and returns the sets in a split list.
        '''
        id = self.exercise_to_index(exercise)

        sql_command = f"select top 1 sets from exercises where exercise = {id} order by day desc;"

        self.__cursor.execute(sql_command)

        set_list = list(self.__cursor)[0][0] # We only want one column
        set_list = list(set_list.split(" "))

        return set_list

    def find_personal_best(self, exercise: str) -> str:
        '''
            This function will find the personal best of a specific 
            exercise.
        '''
        id = self.exercise_to_index(exercise)

        sql_command = f"select record from personal_best where id = {id};"

        self.__cursor.execute(sql_command)

        personal_best = list(self.__cursor)[0][0]

        return personal_best
