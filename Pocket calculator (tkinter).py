import tkinter as tk


class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")

        self.expression = ''
        self.last_string = '0'

        self.text = tk.StringVar()
        self.text.set(self.last_string)
        self.text.trace('w', self.character_limit)

        self.create_entry()
        self.create_buttons()

    def create_entry(self):
        self.entry = tk.Entry(self.master, width=10, textvariable=self.text,
                              font='Helvetica 24', justify='right', takefocus=0)
        self.entry.bind("<Key>", lambda event: "break")  # Disable keyboard.
        self.entry.grid(row=0, column=0, columnspan=5)

    def create_buttons(self):
        buttons_info = [
            ['7', 1, 0], ['8', 1, 1], ['9', 1, 2],
            ['4', 2, 0], ['5', 2, 1], ['6', 2, 2],
            ['1', 3, 0], ['2', 3, 1], ['3', 3, 2],
            ['0', 4, 0], ['C', 4, 1], ['.', 4, 2],
            ['+/-', 4, 3], ['=', 3, 3],
            ['+', 1, 4], ['-', 2, 4], ['*', 3, 4], ['/', 4, 4]
        ]

        self.buttons = [self.create_button(*info) for info in buttons_info]
        for button in self.buttons:
            if button.cget('text').isdigit():
                button.bind('<Button-1>',
                            lambda event, button=button: self.write_digit(button))
            elif button.cget('text') == 'C':
                button.configure(command=self.clear_entry)
            elif button.cget('text') == '.':
                button.configure(command=self.decimal_point)
            elif button.cget('text') == '+/-':
                button.configure(command=self.change_sign)
            elif button.cget('text') == '=':
                button.configure(
                    command=lambda button=button: self.equal_function(button))
            elif button.cget('text') in ['+', '-', '*', '/']:
                button.configure(
                    command=lambda button=button: self.operation_function(button))

    def create_button(self, button_text, row, column):
        button = tk.Button(self.master, text=button_text, width=3,
                           height=2, font='Helvetica 12')
        button.grid(row=row, column=column)
        return button

    def character_limit(self, *args):
        string = self.text.get()
        if len(string) <= 10 and self.last_string:
            self.last_string = string
        else:
            string = self.last_string
            self.text.set(self.last_string)
        return len(string) < 10

    def write_digit(self, button):
        if self.character_limit():
            char = button.cget('text')
            if self.text.get() == '0':
                self.last_string = ''
            self.last_string += char
            self.text.set(self.last_string)
            for button in self.buttons[11:]:
                button.configure(state='normal')

    def clear_entry(self):
        self.expression = ''
        self.last_string = '0'
        self.text.set(self.last_string)
        for button in self.buttons:
            button.configure(state='normal')

    def decimal_point(self):
        string = self.text.get()
        if not self.last_string:
            self.last_string = '0.'
        elif string.count('.') < 1:
            self.last_string += '.'
        self.text.set(self.last_string)

        for button in self.buttons[13:]:
            button.configure(state='normal')

    def change_sign(self):
        string = self.text.get()
        if string != '0':
            if string[0] != '-':
                self.text.set('-' + string)
            else:
                self.text.set(string[1:])

    def equal_function(self, button):
        if self.expression:
            self.expression += self.text.get()
            try:
                result = eval(self.expression)
                if len(str(result)) < 10:
                    self.text.set(str(result))
                else:
                    try:
                        dot = str(result).index('.')
                        rnd = 10 - dot
                        self.text.set(str(round(result, rnd)))
                    except ValueError:
                        for button in self.buttons:
                            if button.cget('text') != 'C':
                                button.configure(state='disabled')
                        self.text.set('Error!')
            except ZeroDivisionError:
                for button in self.buttons:
                    if button.cget('text') != 'C':
                        button.configure(state='disabled')
                self.text.set('Error!')

            for b in self.buttons[12:14]:
                b.configure(state='disabled')
            self.expression = ''
            self.last_string = ''

    def operation_function(self, button):
        self.expression += self.text.get() + button.cget('text')
        for button in self.buttons[12:]:
            button.configure(state='disabled')
        self.last_string = ''


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
