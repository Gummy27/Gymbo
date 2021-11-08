import json
from new_workout import New_workout

class Data_handler:
    def __init__(self) -> None:
        try:
            with open("static/data.json", 'r') as file:
                self.__data = json.load(file)
                self.__personal_bests = self.__data["personal_bests"]
                self.__prev_workouts = self.__data["prev_workouts"]
                self.__exercise_keys = self.__data["exercises"]
        except FileNotFoundError as err:
            print(f"Data handler has crashed: {err}")
            raise
    
    def get_json(self):
        return self.__data
    
    def get_list_of_exercises(self):
        return self.__exercise_keys

    def exercise_to_index(self, exercise):
        return str(self.__exercise_keys.index(exercise))

    def find_prev_workout(self, exercise):
        index = self.exercise_to_index(exercise)

        for date in self.__prev_workouts:
            if index in self.__prev_workouts[date]:
                return date, self.__prev_workouts[date][index]
        return None, None

    def find_personal_best(self, exercise):
        index = self.exercise_to_index(exercise)

        return self.__personal_bests[int(index)]

    def new_personal_best(self, exercise, weight):
        index = self.exercise_to_index(exercise)

        self.__personal_bests[int(index)] = weight

    def add(self, new_workout: New_workout):
        date, sets = new_workout.into_dict()

        self.__prev_workouts[date] = sets

        print(self.__prev_workouts)

    def save_to_file(self):
        file_dict = {}

        file_dict["exercises"] = self.__exercise_keys
        file_dict["personal_bests"] = self.__personal_bests
        file_dict["prev_workouts"] = self.__prev_workouts

        with open("static/data.json", 'w') as file:
            json.dump(file_dict, file)

def main():
    data = Data_handler()   
    new_workout = New_workout("2021-11-2")

    new_workout.add(0, "40x7")
    date, sets = new_workout.into_dict()

    data.add(date, sets)


if __name__ == "__main__":
    main()
