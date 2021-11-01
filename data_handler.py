import json
from new_workout import New_workout

class Data_handler:
    def __init__(self) -> None:
        try:
            with open("static/data.json", 'r') as file:
                data = json.load(file)
                self.__personal_bests = data["personal_bests"]
                self.__prev_workouts = data["prev_workouts"]
                self.__exercise_keys = data["exercises"]
        except FileNotFoundError as err:
            print(f"Data handler has crashed: {err}")
            raise
    
    def get_list_of_exercises(self):
        return self.__exercise_keys

    def exercise_to_index(self, exercise):
        return str(self.__exercise_keys.index(exercise))

    def find_prev_workout(self, exercise):
        index = self.exercise_to_index(exercise)
        print("This is running for some reason!", exercise, index)

        for date in self.__prev_workouts:
            if index in self.__prev_workouts[date]:
                return date, self.__prev_workouts[date][index]
        return None, None

    def find_personal_best(self, exercise):
        index = self.exercise_to_index(exercise)

        return self.__personal_bests[int(index)]

    def add(self, new_workout: New_workout):
        date, sets = new_workout.into_dict()

        self.__prev_workouts[date] = sets

        print(self.__prev_workouts)


def main():
    data = Data_handler()   
    new_workout = New_workout("2021-11-2")

    new_workout.add(0, "40x7")
    date, sets = new_workout.into_dict()

    data.add(date, sets)


if __name__ == "__main__":
    main()
