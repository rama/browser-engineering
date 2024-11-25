import tkinter.font

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18


class Text:
    def __init__(self, text):
        self.text = text


class Tag:
    def __init__(self, tag):
        self.tag = tag


class Layout:
    def __init__(self, tokens):
        self.display_list = []
        self.line = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.size = 12
        self.weight = "normal"
        self.style = "roman"

        for tok in tokens:
            self.token(tok)

        self.flush()

    def flush(self):
        if not self.line:
            return
        metrics = [self.font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])

        baseline = self.cursor_y + 1.25 * max_ascent

        for x, word, self.font in self.line:
            y = baseline - self.font.metrics("ascent")
            self.display_list.append((x, y, word, self.font))
            max_descent = max([metric["descent"] for metric in metrics])
            self.cursor_y = baseline + 1.25 * max_descent

        self.cursor_x = HSTEP
        self.line = []

    def token(self, tok):
        if isinstance(tok, Text):
            for w in tok.text.split():
                self.word(w)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP

    def word(self, word):
        self.font = tkinter.font.Font(
            family="Georgia",
            size=self.size,
            weight=self.weight,
            slant=self.style,
        )
        w = self.font.measure(word)
        if self.cursor_x + w >= WIDTH - HSTEP:
            self.flush()
            self.cursor_y += self.font.metrics("linespace") * 1.25
            self.cursor_x = HSTEP
        self.line.append((self.cursor_x, word, self.font))
        self.cursor_x += w + self.font.measure(" ")


def lex(body):
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out
