import json

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

        for date in self.__prev_workouts:
            if index in self.__prev_workouts[date]:
                return date, self.__prev_workouts[date][index]
        return None, None

    def find_personal_best(self, exercise):
        index = self.exercise_to_index(exercise)

        return self.__personal_bests[int(index)]

def main():
    data = Data_handler()

    print(data.find_personal_best("Bench press"))


if __name__ == "__main__":
    main()
