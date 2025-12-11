'''
todo:
    - implement leading zero option
    - implement icon


bug: no solve_II:
    Se permitir zero à esquerda, a solução não bate.
    Por ex, 4818 minimiza para 688, com 5 movimentos.
    Mas poderia minimizar para 088, se puder zero à esquerda.
    Poderia minimizar para 0044, se tiver que manter comprimento.

    Permitir zero à esquerda não garante que o comprimento da solução será o mesmo que de N.

    Permitir zero à esquerda é diferente de permitir apagar dígitos.

'''

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from constantes import *
from display import Display
from functions import *
from translation import Translator


class Application(ttk.Window):
    def __init__(self):
        super().__init__(resizable=(False, False))

        self.translator = Translator()

        self.title(APP_TITLE)
        self.version = APP_VERSION

        # Icon setup
        # icon_file = "doc/images/icon.png"
        # self.iconphoto(True, tk.PhotoImage(file=icon_file))

        # Style setup
        style = ttk.Style()
        # theme_names = style.theme_names()
        theme_names = ['cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone',
                       'yeti', 'pulse', 'united', 'morph', 'journal', 'simplex', 'cerculean']
        # theme_names += ['darkly', 'superhero', 'solar', 'cyborg', 'vapor']

        self.background_color = style.colors.bg
        self.on_color = style.colors.primary
        self.off_color = style.colors.light
        self.highlight_color = style.colors.warning

        # HEADER FRAME
        header_frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        header_frame.pack(fill=X, expand=NO)

        # Title Label
        game_title = ttk.Label(
            master=header_frame,
            text=APP_TITLE,
            font="-size 24 -weight bold"
        )
        game_title.pack(side=LEFT)

        # Themes Combobox
        theme_cbo = ttk.Combobox(
            master=header_frame,
            text=style.theme.name,
            values=theme_names,
        )
        theme_cbo.current(theme_names.index(style.theme.name))
        theme_cbo.pack(padx=5, side=RIGHT)

        # Theme Label
        self.theme_label = ttk.Label(
            master=header_frame,
            text="Theme:",
            font="-size 10 -weight bold"
        )
        self.theme_label.pack(padx=5, side=RIGHT)

        def change_theme(e):
            ''' Change the theme of the application '''
            t = theme_cbo.get()
            style.theme_use(t)
            theme_cbo.selection_clear()
            # theme_selected.configure(text=t)

            self.on_color = style.colors.primary
            self.off_color = style.colors.light
            self.highlight_color = style.colors.warning
            self.background_color = style.colors.bg

            for j, v in enumerate(self.display_instance.vectors):
                for i, d in enumerate(v):
                    if d == 1:
                        self.display_instance.digits[j].canvas.itemconfig(
                            self.display_instance.digits[j].segments[i], fill=self.on_color)
                    if d == 0:
                        self.display_instance.digits[j].canvas.itemconfig(
                            self.display_instance.digits[j].segments[i], fill=self.off_color)

        theme_cbo.bind('<<ComboboxSelected>>', change_theme)

        ttk.Separator(self).pack(fill=X, pady=5, padx=10)

        # MAIN FRAME
        ''' Inside the Main Frame, there are two frames: lframe and rframe. '''
        self.main_frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        self.main_frame.pack(fill=BOTH, expand=YES)

        # rframe: OPTIONS
        self.rframe = ttk.LabelFrame(
            self.main_frame, padding=(10, 10, 10, 10),  text='Options')
        self.rframe.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5)

        # lframe: BUTTONS AND INFO
        self.lframe = ttk.LabelFrame(
            self.main_frame, padding=(10, 10, 10, 10),  text='Game')
        self.lframe.pack(side=TOP, fill=BOTH, expand=YES, padx=5)

        # Implementing Options in rframe
        # Keep lenght setup
        self.keep_lenght = tk.BooleanVar(value=False)
        self.keep_lenght_checkbutton = ttk.Checkbutton(
            master=self.rframe,
            text="Keep the number of digits",
            variable=self.keep_lenght,
        )
        self.keep_lenght_checkbutton.grid(
            row=0, column=1, pady=5, padx=10, sticky='w')

        # Keep parity setup
        self.keep_parity = tk.BooleanVar(value=False)
        self.keep_parity_checkbutton = ttk.Checkbutton(
            master=self.rframe,
            text="Keep the number's parity",
            variable=self.keep_parity,
            state=NORMAL,
        )
        self.keep_parity_checkbutton.grid(
            row=1, column=1, pady=5, padx=10, sticky='w')

        # Leading zero setup (to be implemented)
        def leading_zero_cb():
            print(f'Leading zero: {self.leading_zero.get()}')

        self.leading_zero = tk.BooleanVar(value=False)
        self.leading_zero_checkbutton = ttk.Checkbutton(
            master=self.rframe,
            text="Allow leading zeros",
            variable=self.leading_zero,
            command=leading_zero_cb,
            state=DISABLED
        )
        self.leading_zero_checkbutton.grid(
            row=2, column=1, pady=5, padx=10, sticky='w')

        # Set initial number setup
        vcmd = (self.register(self.validate_input), "%P")

        def fix_initial_number_cb():
            print(f'Fix initial number: {self.fix_initial_number.get()}')
            if self.fix_initial_number.get():
                self.fix_initial_number_input.config(state='normal')
                self.fix_initial_number_input.focus_set()
            else:
                self.fix_initial_number_input.config(state='disabled')

        def fix_initial_number_return(event):
            ''' Callback to set initial number '''
            if self.fix_initial_number.get() and self.validate_input(self.fix_initial_number_input.get()) and self.fix_initial_number_input.get() != '':
                self.new_game()

        self.fix_initial_number = tk.BooleanVar(value=False)
        self.fix_initial_number_checkbutton = ttk.Checkbutton(
            master=self.rframe,
            text="Set initial number",
            variable=self.fix_initial_number,
            command=fix_initial_number_cb
        )
        self.fix_initial_number_checkbutton.grid(
            row=3, column=1, pady=5, padx=10, sticky='w'
        )
        self.fix_initial_number_input = ttk.Entry(
            master=self.rframe,
            textvariable=tk.StringVar(value=1234),
            state='disabled',
            width=6,
            validate="key",  # Enable validation on keypress
            validatecommand=vcmd  # Use the registered validation function
        )
        self.fix_initial_number_input.grid(
            row=3, column=2,  pady=5, padx=5, sticky='w'
        )
        self.fix_initial_number_input.bind(
            '<Return>', fix_initial_number_return)
        self.fix_initial_number_input.bind(
            '<KP_Enter>', fix_initial_number_return)

        # Maximal number of moviments setup
        self.max_num_moviments_label = ttk.Label(
            master=self.rframe,
            text=f"Maximum number of moves:\n(Game II)",
        )
        self.max_num_moviments_label.grid(
            row=4, column=1, pady=5, padx=10, sticky='w'
        )
        self.max_num_moviments = tk.IntVar(
            value=3)  # default value
        self.max_num_moviments_spinbox = ttk.Spinbox(
            master=self.rframe,
            from_=1,
            to=max_num_moviments,
            textvariable=self.max_num_moviments,
            width=3,
            state=DISABLED
        )
        self.max_num_moviments_spinbox.grid(
            row=4, column=2, pady=5, padx=5, sticky='w'
        )

        # Exact number of moviments setup
        self.exact_moviments_label = ttk.Label(
            master=self.rframe,
            text=f"Precise number of moves:\n(Game III)",
        )
        self.exact_moviments_label.grid(
            row=5, column=1, pady=5, padx=10, sticky='w'
        )
        self.exact_moviments = tk.IntVar(
            value=3)  # default value
        self.exact_moviments_spinbox = ttk.Spinbox(
            master=self.rframe,
            from_=1,
            to=max_num_moviments,
            textvariable=self.exact_moviments,
            width=3,
            state=DISABLED
        )
        self.exact_moviments_spinbox.grid(
            row=5, column=2, pady=5, padx=5, sticky='w'
        )

        # Solver setup on lframe
        self.solver_group = ttk.Labelframe(
            master=self.rframe,
            text="Choose a Game",
            padding=(10, 10, 10, 10)
        )
        self.solver_group.grid(row=0, column=0, rowspan=6, sticky="ns")

        self.solvers_list = list(solvers.keys())
        self.solver_choice = tk.StringVar()
        self.solver_choice.set(self.solvers_list[0])
        self.solver = solvers[self.solver_choice.get()]

        self.menu_solvers = ttk.Menu(self.solver_group, tearoff=0)
        for t in self.solvers_list:
            translated = self.translator.translate(t)
            self.menu_solvers.add_radiobutton(
                label=translated,
                value=t,
                command=lambda opt=t: self.update_solver(opt)
            )

        self.menubutton = ttk.Menubutton(
            master=self.solver_group,
            textvariable=self.solver_choice,
            bootstyle=PRIMARY,
            text=f"{self.translator.translate('choose_game_label')}",
            menu=self.menu_solvers,
        )
        self.menubutton.pack(fill=X, pady=0)

        # Help Text
        self.txt = ttk.Text(
            master=self.solver_group,
            height=7,
            width=60,
            wrap='word',
        )

        self.txt.insert(
            END, solvers_help[self.translator.current_language][self.solver_choice.get()])
        self.txt.pack(
            side=BOTTOM,
            anchor=NW,
            pady=5,
            fill=BOTH,
            expand=YES
        )
        self.txt.config(state="disabled")

        # Game Buttons Frame
        self.game_buttons_frame = ttk.Frame(self.lframe)
        self.game_buttons_frame.pack(side="top", fill=tk.X)

        # Button to start new game
        self.button_new_game = ttk.Button(
            self.game_buttons_frame,
            text="New Game",
            command=self.new_game,
        )
        self.button_new_game.pack(padx=5, pady=5, side="left")

        # Button to reset the game
        self.button_repeat_game = ttk.Button(
            self.game_buttons_frame,
            text="Reset Game",
            command=lambda: self.new_game(repeat=True),
        )
        self.button_repeat_game.pack(padx=5, pady=5, side="left")

        # Button to check solution
        self.button_check_solution = ttk.Button(
            self.game_buttons_frame,
            text="Check Solution",
            command=self.check_solution,
        )
        self.button_check_solution.pack(padx=5, pady=5, side="left")

        ttk.Separator(self.lframe).pack(fill=X, pady=10, padx=5)

        # Timer info
        self.clock_on = False
        self.time = tk.IntVar(value=0)
        self.formatted_time = tk.StringVar()
        self.formatted_time.set(
            f"{self.translator.translate('Time')}: {seconds_to_time(self.time.get())}")
        self.label_time = ttk.Label(
            self.lframe,
            textvariable=self.formatted_time,
            font='-size 14 -weight bold'
        )

        # Moviments info
        self.moviments = tk.IntVar(value=0)
        self.formatted_moviments = tk.StringVar()
        self.formatted_moviments.set(
            f"{self.translator.translate('Moviments')}: {self.moviments.get()}")
        self.label_moviments = tk.Label(
            self.lframe,
            textvariable=self.formatted_moviments,
            font='-size 14 -weight bold'
        )

        # Initial Number info
        self.initial_number = tk.IntVar(value=random_number())
        self.formatted_initial_number = tk.StringVar()
        self.formatted_initial_number.set(
            f"{self.translator.translate('Initial Number')}: {self.initial_number.get()}")
        self.label_initial_number = tk.Label(
            self.lframe,
            textvariable=self.formatted_initial_number,
            font='-size 14 -weight bold'
        )

        # Create a label with hidden text to be used as a tooltip
        self.hide_solution_label = ttk.Label(
            self.lframe,
            text="",
            font="-size 14 -weight bold"
        )

        # Bind mouse hover events
        self.hide_solution_label.bind("<Enter>", self.show_text)
        self.hide_solution_label.bind("<Leave>", self.hide_text)

        # Packing info labels
        self.label_initial_number.pack(
            padx=5, pady=5, side="top")

        self.label_moviments.pack(
            padx=5, pady=5, side="top")

        self.label_time.pack(
            padx=5, pady=5, side="top")

        self.hide_solution_label.pack(
            padx=5, pady=5, side="top")

        # DISPLAY FRAME
        ''' Inside the Display Frame, there is a Display instance. '''

        self.bg_color = style.lookup("TLabelFrame", "background")

        self.display_frame = ttk.LabelFrame(
            self, text='Display', padding=(10, 10, 10, 10))
        self.display_frame.pack(side='top', fill=X,
                                expand=TRUE, padx=15, pady=10)

        # BOTTOM FRAME
        ''' Inside the Bottom Frame, there are two labels: author_label and version_label. '''

        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side='bottom', padx=0, pady=0,
                               fill=tk.X, expand=False)
        ttk.Separator(self.bottom_frame).pack(fill=X, pady=5, padx=5)

        # Author label
        self.author_label = ttk.Label(
            self.bottom_frame,
            text=f"{self.translator.translate('author_label')}: " + APP_AUTHOR,
        )
        self.author_label.pack(side='left', pady=5, padx=5)

        # Version label
        self.version_label = ttk.Label(
            self.bottom_frame,
            text=f"{self.translator.translate('Version')}: " +
            str(self.version),
        )
        self.version_label.pack(side='right', pady=5, padx=5)

        self.display_instance = None
        self.label_ans = None

        # Trace variables
        self.moviments.trace_add("write",
                                 self.update_label_moviments)
        self.initial_number.trace_add("write",
                                      self.update_label_initial_number)

        self.rebuild_menu()
        self.update_ui()
        self.clock()  # requires label_time
        self.new_game()

    def show_text(self, event):
        self.hide_solution_label.config(text="fooo")

    def hide_text(self, event):
        self.hide_solution_label.config(text="")

    def validate_input(self, new_value):
        return (new_value.isdigit() and len(new_value) <= len(str(initial_number_max))) or new_value == ''

    def update_solver(self, new_solver):
        self.solver = solvers[new_solver]
        self.solver_choice.set(new_solver)
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.insert(
            "1.0", solvers_help[self.translator.current_language][self.solver_choice.get()])
        self.txt.config(state="disabled")
        if new_solver == 'Game I':
            self.max_num_moviments_spinbox.config(state=DISABLED)
            self.exact_moviments_spinbox.config(state=DISABLED)
        if new_solver == 'Game II':
            self.exact_moviments_spinbox.config(state=DISABLED)
            self.max_num_moviments_spinbox.config(state=NORMAL)
            self.max_num_moviments_spinbox.focus_set()
        if new_solver == 'Game III':
            self.max_num_moviments_spinbox.config(state=DISABLED)
            self.exact_moviments_spinbox.config(state=NORMAL)
            self.exact_moviments_spinbox.focus_set()

    def new_game(self, repeat=False):
        if self.display_instance:
            self.display_instance.destroy()

        if self.label_ans:
            self.label_ans.destroy()

        self.moviments.set(0)
        self.formatted_moviments.set(
            f"{self.translator.translate('Moviments')}: {self.moviments.get()}"
        )

        if not repeat:
            if self.fix_initial_number.get() and self.validate_input(self.fix_initial_number_input.get()):
                self.initial_number.set(
                    int(self.fix_initial_number_input.get()))
            else:
                self.initial_number.set(random_number())

        # Display instance
        self.display_instance = Display(
            master=self.display_frame, root=self,  number=self.initial_number.get())
        self.display_instance.pack(side=BOTTOM)

        self.formatted_initial_number.set(
            f"{self.translator.translate('Initial Number')}: {self.initial_number.get()}"
        )

        self.time.set(0)
        self.clock_on = True

        self.label_ans = ttk.Label(
            self, text='', font='-size 14 -weight bold')
        self.label_ans.pack(pady=0)

    def clear_ans_label(self):
        self.label_ans.configure(text=f"")

    def check_solution(self, *args, **kwargs):
        self.display_instance.update_display()
        user_solution = self.display_instance.number

        ''' Compute the solution and the minimum number of moviments using the solver from solver menu '''
        self.solution, self.min_moviments = self.solver(
            self.initial_number.get(),
            exact_moviments=self.exact_moviments.get(),
            keep_lenght=self.keep_lenght.get(),
            keep_parity=self.keep_parity.get(),
            leading_zero=self.leading_zero.get(),
            max_num_moviments=self.max_num_moviments.get(),
            num_moviments=self.moviments.get(),
        )
        print(self.display_instance.__str__())

        # Solver I setup
        # No restrictions on number of moviments
        if self.solver_choice.get() == 'Game I':
            if self.solution == user_solution:
                self.clock_on = False
                if self.min_moviments == self.moviments.get():
                    self.label_ans.configure(
                        text=f"{self.translator.translate('Perfect')}: {self.solution}",
                        foreground=self.style.colors.success
                    )
                if self.min_moviments < self.moviments.get():
                    self.label_ans.configure(
                        text=f"{self.translator.translate('Correct')}: {self.solution}. {self.translator.translate('But too many moviments')}: {self.moviments.get()}", foreground=self.style.colors.warning
                    )
            else:
                self.label_ans.configure(
                    text=f"{self.translator.translate('Not Yet. Try again!')}",
                    foreground=self.style.colors.warning
                )
                self.after(2000, self.clear_ans_label)

            return None

        # Solver II setup
        # Number of moviments must be less than or equal to the maximum allowed
        if self.solver_choice.get() == 'Game II':
            if self.moviments.get() > self.max_num_moviments.get():
                self.label_ans.configure(
                    text=f"{self.translator.translate('Sorry. Too many moviments!')} {self.moviments.get()}. {self.translator.translate('Maximum allowed')}: {self.max_num_moviments.get()}", foreground=self.style.colors.warning
                )
                return None
            if self.solution == user_solution:
                self.clock_on = False
                if self.moviments.get() == self.min_moviments:
                    self.label_ans.configure(
                        text=f"{self.translator.translate('Perfect')}: {self.solution}",
                        foreground=self.style.colors.success
                    )
                else:
                    ''' TODO: neste caso, decidir o que avisar, pois pode ser que tenha chego no menor num mas não com o mov ideal, porém ainda dentro do lim max. por ex, 123 com max 4 minimza pra 28 com 2 mas pode min pra 38 com 3'''
                    self.label_ans.configure(
                        text=f"{self.translator.translate('Correct')}: {self.solution}. {self.translator.translate('But too many moviments')}: {self.moviments.get()}", foreground=self.style.colors.warning
                    )
            else:
                self.label_ans.configure(
                    text=f"{self.translator.translate('Not Yet. Try again!')}",
                    foreground=self.style.colors.warning
                )
                self.after(2000, self.clear_ans_label)
            return None

        # Solver III setup
        # Number of moviments must be exactly the same as the expected
        if self.solver_choice.get() == 'Game III':
            if self.moviments.get() != self.exact_moviments.get():
                self.label_ans.configure(
                    text=f"{self.translator.translate('Sorry. You must move exactly')} {self.exact_moviments.get()} {self.translator.translate('segments')}.", foreground=self.style.colors.warning
                )
                self.after(2000, self.clear_ans_label)
                return None
            if self.solution == user_solution:
                self.clock_on = False
                self.label_ans.configure(
                    text=f"{self.translator.translate('Perfect')}: {self.solution}",
                    foreground=self.style.colors.success
                )
            else:
                self.label_ans.configure(
                    text=f"{self.translator.translate('Not Yet. Try again!')}",
                    foreground=self.style.colors.warning
                )
                self.after(2000, self.clear_ans_label)
            return None

    def clock(self):
        if self.clock_on:
            self.time.set(self.time.get() + 1)
            self.formatted_time.set(
                f"{self.translator.translate('Time')}: {seconds_to_time(self.time.get())}"
            )
        self.label_time.after(1000, self.clock)

    def update_label_moviments(self, *args):
        self.formatted_moviments.set(
            f"{self.translator.translate('Moviments')}: {self.moviments.get()}"
        )

    def update_label_initial_number(self, *args):
        self.formatted_initial_number.set(
            f"{self.translator.translate('Initial Number')}: {self.initial_number.get()}"
        )

    def rebuild_menu(self):
        menubar = ttk.Menu(self)

        # Menu
        file_menu = ttk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label=self.translator.translate('exit'), command=self.quit)
        menubar.add_cascade(label='Menu', menu=file_menu)

        # Language Menu
        language_menu = ttk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.translator.translate(
            'language'), menu=language_menu)
        # SubMenu
        language_menu.add_command(label=self.translator.translate(
            'english'), command=lambda: self.change_language('en'))
        language_menu.add_command(label=self.translator.translate(
            'italian'), command=lambda: self.change_language('it'))
        language_menu.add_command(label=self.translator.translate(
            'portuguese'), command=lambda: self.change_language('pt'))

        self.config(menu=menubar)

    def update_ui(self):
        self.theme_label.config(text=self.translator.translate('Theme'))
        self.rframe.config(text=self.translator.translate('Options'))
        self.lframe.config(text=self.translator.translate('Game'))
        self.keep_lenght_checkbutton.config(
            text=self.translator.translate('keep_lenght_checkbutton'))
        self.keep_parity_checkbutton.config(
            text=self.translator.translate('keep_parity_checkbutton'))
        self.leading_zero_checkbutton.config(
            text=self.translator.translate('leading_zero_checkbutton'))
        self.fix_initial_number_checkbutton.config(
            text=self.translator.translate('fix_initial_number_checkbutton'))
        self.max_num_moviments_label.config(
            text=self.translator.translate('max_num_moviments_label'))
        self.exact_moviments_label.config(
            text=self.translator.translate('exact_moviments_label'))
        self.solver_group.config(
            text=self.translator.translate('choose_game_label'))
        self.button_new_game.config(
            text=self.translator.translate('new_game_button'))
        self.button_repeat_game.config(
            text=self.translator.translate('button_repeat_game'))
        self.button_check_solution.config(
            text=self.translator.translate('button_check_solution'))
        self.formatted_moviments.set(
            f"{self.translator.translate('Moviments')}: {self.moviments.get()}")
        self.formatted_time.set(
            f"{self.translator.translate('Time')}: {seconds_to_time(self.time.get())}")
        self.formatted_initial_number.set(
            f"{self.translator.translate('Initial Number')}: {self.initial_number.get()}")
        self.display_frame.config(
            text=self.translator.translate('display_frame'))
        self.author_label.config(
            text=f"{self.translator.translate('author_label')}: " + APP_AUTHOR)
        self.version_label.config(
            text=f"{self.translator.translate('Version')}: " + str(self.version))

        # update solver help text
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.insert(
            END, solvers_help[self.translator.current_language][self.solver_choice.get()]
        )
        self.txt.config(state="disabled")

        # Update menubutton
        self.menubutton.config(
            text=self.translator.translate(self.solver_choice.get()))

        # Update translated menu items
        self.menu_solvers.delete(0, "end")
        for t in self.solvers_list:
            self.menu_solvers.add_radiobutton(
                label=self.translator.translate(t),
                value=t,
                command=lambda opt=t: self.update_solver(opt)
            )

        self.rebuild_menu()

    def change_language(self, lang):
        self.translator.set_language(lang)
        self.update_ui()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
