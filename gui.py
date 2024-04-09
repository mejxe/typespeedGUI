import random
import time
from score import Score
from customtkinter import *


slowa = open("words.txt").read().splitlines()
random.shuffle(slowa)
FONT = ("Banschrift",35,"normal")
class Gui:
    def __init__(self):
        self.root = CTk()
        self.root.geometry("800x400+560+340")
        self.root.resizable(False,False)
        self.root.title("TypeSpeed")
        # Frames
        self.textframe = CTkFrame(self.root)
        self.textframe.configure(fg_color="red",bg_color="red",width=760, height=250)
        self.textframe.place(x=20,y=20)
        self.textframe.pack_propagate(False)
        self.typeframe = CTkFrame(self.root)
        self.typeframe.configure(fg_color="blue", bg_color="blue", width=360, height=75)
        self.typeframe.place(x=225, y=305)

        # words
        self.text_placeholder = CTkTextbox(self.textframe,width=760, height=250, corner_radius=0,border_width=0, font=FONT, wrap='word')
        self.text_placeholder.pack()



        self.text_placeholder.insert(1.0,"Press Space to start!")
        # entry window to input words that are on screen
        self.input_entry = CTkEntry(self.typeframe,width=320, height=60,placeholder_text="type here.",font=FONT, border_width=0, corner_radius=0, fg_color="#352F44")
        self.input_entry.pack()
        self.input_entry.bind("<space>", command=self.input_check)




        self.timer = CTkLabel(self.root, text="00:00",font=FONT)
        self.timer.place(x=620, y=315)
        self.text_placeholder.tag_config("wrong", foreground="red")
        self.text_placeholder.tag_config("correct", foreground="#9290C3")
        # variables
        self.timer_on = False
        self.words_correct = 0
        self.words_misspelled = 0
        self.cleared = False
        self.completed = False
        self.ready = True




        self.root.mainloop()


    def create_text(self,text):
        self.text_on_screen = text
        self.highlight_index1 = 0
        self.highlight_index2 = len(self.text_on_screen[0]) + 1
        self.text_placeholder.insert(0.0,text)
        self.text_placeholder.tag_config("first", background="#5C5470")
        self.text_placeholder.tag_add("first",f"1.{0}", f"1.{len(self.text_on_screen[0])}")
        self.text_placeholder.configure(state=DISABLED)



    def update_text(self, word):
        self.text_placeholder.configure(state=NORMAL)
        # remove tag
        self.text_placeholder.tag_remove("first", index1=f"1.{self.highlight_index1}",
                                         index2=f"1.{self.highlight_index2}")
        # update list and screen
        self.text_on_screen.append(word)
        self.text_placeholder.insert(END," "+word)
        self.previous_word = self.text_on_screen.pop(0)
        # add tag
        self.highlight_index1 += len(self.previous_word)+1
        self.highlight_index2 += len(self.text_on_screen[0])+1
        self.text_placeholder.tag_add("first", f"1.{self.highlight_index1}", f"1.{self.highlight_index2-1}")
        self.text_placeholder.configure(state=DISABLED)

    def start_test(self):
        self.create_text(slowa[0:30])
        self.timer_on = True
        self.countdown(30)
        self.input_entry.configure(state=NORMAL)



    def check_spelling(self, inputted_word):
        # restart
        if self.completed:
            self.reset()
            # start the countdown
        if not self.timer_on:
            self.start_test()
            #

        else:

            ### delete excess text

            self.text_placeholder.configure(state=NORMAL)
            if self.highlight_index2 > 200:
                self.text_placeholder.delete("1.0", f"1.{self.highlight_index2 - len(self.text_on_screen[0]) - 1}")
                self.highlight_index2 = len(self.text_on_screen[0]) + 1
                self.highlight_index1 = 0
            self.text_placeholder.configure(state=DISABLED)

            ###

            #### check if correct
            if inputted_word.strip() == self.text_on_screen[0]:
                self.text_placeholder.tag_add("correct",f"1.{self.highlight_index1}",f"1.{self.highlight_index2}")
                self.words_correct += 1*len(self.text_on_screen[0])
                print(self.words_correct)

            else:
                self.text_placeholder.tag_add("wrong",f"1.{self.highlight_index1}",f"1.{self.highlight_index2}")
                self.words_misspelled += self.check_wrong_chars(inputted_word=inputted_word.strip(), expected_word=self.text_on_screen[0])
                print(self.words_misspelled)

            ## add next word and clear the entry
            self.clear_entry()
            self.update_text(slowa[random.randint(0, 2999)])
            ##
    def input_check(self, event):
        if self.ready:
            self.check_spelling(self.input_entry.get())
        else:
            pass
    def clear_entry(self):
        self.input_entry.configure(state=NORMAL)
        self.input_entry.delete(0, END)

    def clear_text(self):
        self.text_placeholder.configure(state=NORMAL)
        self.text_placeholder.delete(1.0, END)
        self.text_on_screen = []




    def countdown(self,time):
        self.time = time
        if self.time >= 0:
            self.after_id = self.timer.after(1000, self.countdown, self.time - 1)
            self.timer.configure(text=f"00:{self.time:02}")
        else:
            self.times_up()

    def getready(self):
        self.ready = True
    def times_up(self):
        self.score = Score(correct=self.words_correct, wrong=self.words_misspelled)
        self.input_entry.configure(state=DISABLED)
        self.text_placeholder.configure(state=NORMAL)
        self.text_placeholder.delete(1.0,END)
        self.text_placeholder.insert(1.0, self.score.generate_score_message())
        self.timer_on = False
        self.completed = True
        self.ready = False
        self.root.after(1500,self.getready)
        self.text_placeholder.configure(state=DISABLED)

    def check_wrong_chars(self, inputted_word, expected_word):
        wrongs = 0
        for i in range(len(expected_word)):
            # try:
            if i<len(inputted_word)-1 and i <len(expected_word)-1:
                if inputted_word[i] != expected_word[i]:
                    wrongs += 1
            # except IndexError:

        return wrongs + abs(len(expected_word)-len(inputted_word))

    def reset(self):
        self.clear_text()
        self.clear_entry()
        random.shuffle(slowa)
        self.create_text(slowa[0:30])
        self.completed = False
        self.words_correct = 0
        self.words_misspelled = 0
        self.highlight_index1 = 0
        self.highlight_index2 = len(self.text_on_screen[0])+1

