class New_workout:
    def __init__(self, date) -> None:
        self.date = date
        self.exercises = {}

    def add(self, tag, set):
        if tag in self.exercises:
            self.exercises[tag].append(set)
        else:
            self.exercises[tag] = [set]

    def into_dict(self):
        my_dict = {}
        my_dict[self.date] = self.exercises

        return my_dict
    
    def clear(self):
        self.exercises = {}

if __name__ == "__main__":
    new_workout = New_workout("2021-11-1")

    print(new_workout.into_dict())