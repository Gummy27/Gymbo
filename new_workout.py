class New_workout:
    def __init__(self, date) -> None:
        self.date = date
        self.exercises = {}

    def add(self, exercise_tag, set):
        if exercise_tag in self.exercises:
            self.exercises[exercise_tag].append(set)
        else:
            self.exercises[exercise_tag] = [set]

    def into_dict(self):

        return self.date, self.exercises
    
    def clear(self):
        self.exercises = {}

    def current_exercise(self, exercise_tag):
        try:
            return self.exercises[exercise_tag]
        except KeyError:
            return None

if __name__ == "__main__":
    new_workout = New_workout("2021-11-1")

    print(new_workout.into_dict())