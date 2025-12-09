# https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html
# https://tkinterexamples.com/events/

# import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from constantes import *
from functions import *
from digit import *


class Display(ttk.Frame):
    def __init__(self, master=None, root=None, number=8, **kwargs):
        super().__init__(master, **kwargs)

        self.root = root
        self.number = number
        self.factors = euclid(norm(number), k=7)
        self.digits = []
        self.vectors = []
        self.states = {}
        self.stack = []
        self.norma = 0
        self.width = 0
        self.height = 0
        # self.solution = self.root.solution
        # self.min_moviment = solve_I(self.number)[1]

        self.background_color = self.root.background_color
        self.on_color = self.root.on_color
        self.off_color = self.root.off_color
        self.highlight_color = self.root.highlight_color

        self.config(padding=(0, 0))

        # Populate digits on display
        for i, d in enumerate(str(self.number)):
            self.digits.append(
                Digit(self, value=int(d), digit_id=i, root=self.root))
            self.vectors.append(self.digits[-1].vector)
            self.norma += sum(self.vectors[-1])

        # Display width and height to adjust root window geometry
        self.width = max(len(self.vectors) * digit_width + 20, 600)
        self.height = digit_height + 00
        # self.root.geometry(f"{self.width}x{self.height}")  # +800+200

        # print(self.__str__())

    def __str__(self):
        self.info = f"""
Display Info
==========={'='*len(str(self.number))}
   Number: {self.number}
     Norm: {self.norma}
   Factor: {self.factors[1]} + {self.factors[0]}x7
Moviments: {self.root.moviments.get()}
   Solver: {self.root.solver_choice.get()}
"""
#Geometry: {self.width}x{self.height}
#Vectors: {self.vectors}
# Solution: {self.root.solution} with {self.root.min_moviments} moviments
        return self.info

    def update_display(self):
        ''' Update display number and vectors '''

        self.number = int(''.join([str(d.value) for d in self.digits]))
        self.vectors = [d.vector for d in self.digits]
        self.norma = sum(sum(v) for v in self.vectors)

    def swap_segments(self, digit_id, event):
        current_digit = self.digits[digit_id]  # Digit object
        current_canvas = current_digit.canvas  # Canvas object

        for segment in current_digit.segments:
            if current_canvas.bbox(segment)[0] <= event.x <= current_canvas.bbox(segment)[2] and current_canvas.bbox(segment)[1] <= event.y <= current_canvas.bbox(segment)[3]:
                # Trazer o segmento clicado para o topo
                current_canvas.tag_raise(segment)
                if self.stack == [] and self.states[(digit_id, segment)] == 0:
                    return

                # nada em mãos e cliquei em aceso
                if self.stack == [] and self.states[(digit_id, segment)] == 1:
                    self.stack.append((digit_id, segment))
                    current_canvas.itemconfig(
                        segment, outline=self.highlight_color)
                    return

                # tem algo em mãos e cliquei no mesmo
                if self.stack[-1] == (digit_id, segment):
                    self.stack.pop()
                    current_canvas.itemconfig(
                        segment, outline=self.background_color)
                    return

                # tem algo em mãos e cliquei em outro apagado
                # somente aqui incrementa o num movimento
                # ao atualizar os vetores de saída e chegada
                # preciso verificar se é um dígito válido para atualizar o digit.value
                if self.states[(digit_id, segment)] == 0:
                    # apagar o de saída
                    self.digits[self.stack[-1][0]].canvas.itemconfig(self.stack[-1][1],
                                                                     outline=self.background_color, fill=self.off_color)
                    self.states[self.stack[-1]] = 0
                    self.digits[self.stack[-1][0]
                                ].vector[self.stack[-1][1] - 1] = 0  # subtract 1 from index

                    num = vec_to_digit(self.digits[self.stack[-1][0]].vector)
                    if num != None:
                        self.digits[self.stack[-1][0]].value = num

                    # acender o de chegada
                    current_canvas.itemconfig(
                        segment, outline=self.background_color, fill=self.on_color)
                    self.states[(digit_id, segment)] = 1
                    self.digits[digit_id].vector[segment-1] = 1

                    num = vec_to_digit(self.digits[digit_id].vector)
                    if num != None:
                        self.digits[digit_id].value = num

                    self.root.moviments.set(self.root.moviments.get() + 1)
                    self.stack.pop()
                    return

                # tem algo em mãos e cliquei em outro aceso
                if self.states[(digit_id, segment)] == 1:
                    self.digits[self.stack[-1][0]].canvas.itemconfig(self.stack[-1][1],
                                                                     outline=self.background_color)
                    self.stack.pop()

                    self.stack.append((digit_id, segment))
                    current_canvas.itemconfig(
                        segment, outline=self.highlight_color)
                    return


if __name__ == "__main__":
    None
