import tkinter as tk
from constantes import *
from functions import *


class Digit:
    def __init__(self, master, value, digit_id, root=None):
        self.root = root
        self.master = master
        self.value = value
        self.digit_id = digit_id
        self.vector = vectors[self.value].copy()
        self.segments = []

        self.background_color = self.root.background_color
        self.on_color = self.root.on_color
        self.off_color = self.root.off_color
        self.highlight_color = self.root.highlight_color

        self.canvas = tk.Canvas(master,
                                width=digit_width,
                                height=digit_height,
                                background=self.background_color,
                                takefocus=False
                                # highlightthickness=2,
                                # relief='flat'
                                # border=0,
                                # borderwidth=0,
                                # highlightbackground='red',
                                # highlightcolor='yellow'
                                )
        self.canvas.pack(side="left", pady=0, padx=0)
        self.canvas.bind("<Button-1>", self.swap_segments)

        # Do not change orders
        self.create_segment(
            'vertical', centers[0], segment_id=0, color=self.off_color)
        self.create_segment(
            'vertical', centers[1], segment_id=1, color=self.off_color)
        self.create_segment(
            'horizontal', centers[2], segment_id=2, color=self.off_color)
        self.create_segment(
            'horizontal', centers[3], segment_id=3, color=self.off_color)
        self.create_segment(
            'horizontal', centers[4], segment_id=4, color=self.off_color)
        self.create_segment(
            'vertical', centers[5], segment_id=5, color=self.off_color)
        self.create_segment(
            'vertical', centers[6], segment_id=6, color=self.off_color)

        background = self.canvas.create_rectangle(
            0, 0, digit_width, digit_height,
            # fill=background_color,
            width=0,
            tags="background",
            state="disabled",
            disabledfill=self.background_color,
            outline=self.background_color,
        )
        self.canvas.tag_lower(background)

        self.animate_segment()

    def swap_segments(self, event):
        self.master.swap_segments(self.digit_id, event)

    def create_segment(self, orientation, center, segment_id, color=None):
        ox = center[0]
        oy = center[1]

        if orientation == 'horizontal':
            self.segment = self.canvas.create_polygon(
                ox - segment_length // 2, oy - segment_thickness // 2,
                ox + segment_length // 2, oy - segment_thickness // 2,
                ox + segment_length // 2 + segment_tail, oy,
                ox + segment_length // 2, oy + segment_thickness // 2,
                ox - segment_length // 2, oy + segment_thickness // 2,
                ox - segment_length // 2 - segment_tail, oy,
                width=3,
                fill=color,
                outline=self.background_color,
                tags=["segment", "horizontal"]
            )
        elif orientation == 'vertical':
            self.segment = self.canvas.create_polygon(
                ox - segment_thickness // 2, oy - segment_length // 2,
                ox, oy - segment_length // 2 - segment_tail,
                ox + segment_thickness // 2, oy - segment_length // 2,
                ox + segment_thickness // 2, oy + segment_length // 2,
                ox, oy + segment_length // 2 + segment_tail,
                ox - segment_thickness // 2, oy + segment_length // 2,
                width=3,
                fill=color,
                outline=self.background_color,
                tags=["segment", "vertical"]
            )
        self.segments.append(self.segment)
        self.master.states[(self.digit_id, self.segment)
                           ] = self.vector[segment_id]
        return None

    def animate_segment(self, idx=0):
        if idx < 6:
            current_segment = self.segments[(
                segment_animation_order[idx % 7] - 1) % 7]
            self.canvas.itemconfig(current_segment, fill=self.on_color)

            self.master.after(segment_animation_speed,
                              self.animate_segment, idx + 1)
        if 5 < idx < 13:
            current_segment = self.segments[(
                segment_animation_order[idx % 7]-1) % 7]
            self.canvas.itemconfig(current_segment, fill=self.off_color)

            self.master.after(segment_animation_speed,
                              self.animate_segment, idx + 1)
        if idx == 13:
            for i, d in enumerate(self.vector):
                if d == 1:
                    self.canvas.itemconfig(
                        self.segments[i], fill=self.on_color)
                if d == 0:
                    self.canvas.itemconfig(
                        self.segments[i], fill=self.off_color)
