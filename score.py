from customtkinter import *

FONT = ("Banschrift",20,"normal")
class Score():
    def __init__(self, correct, wrong):
        self.correct = correct
        self.wrong = wrong
        self.wpm = self.calculate_wpm()
        self.accuracy = self.calculate_accuraccy()
        self.adj_wpm = self.calculate_adjusted_wpm()

    def calculate_wpm(self):
        return (self.correct/5)/0.5

    def calculate_accuraccy(self):
        return self.correct/(self.correct+self.wrong)

    def calculate_adjusted_wpm(self):
        return abs(round(self.accuracy*self.wpm))

    def generate_score_message(self):
        return (f"Great job! Your wpm is {self.adj_wpm}!\nAccuracy: {round(self.accuracy,2)*100}%\nMistakes:{self.wrong}\n\nTo try again press space!")

