import tkinter
import tkinter.font
from url import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.bodyfont = tkinter.font.Font(
            family="Georgia",
            size=16,
        )

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def load(self, url):
        body = url.request()
        text = url.lex(body)

        self.display_list = self.layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(
                x,
                y - self.scroll,
                text=c,
                font=self.bodyfont,
                anchor="nw",
            )

    def layout(self, text):
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP
        for word in text.split():
            w = self.bodyfont.measure(word)
            if cursor_x + w >= WIDTH - HSTEP:
                cursor_y += self.bodyfont.metrics("linespace") * 1.25
                cursor_x = HSTEP
            display_list.append((cursor_x, cursor_y, word))
            cursor_x += w + self.bodyfont.measure(" ")
        return display_list


if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
