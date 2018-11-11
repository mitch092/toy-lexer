from enum import Enum
keywords = ["int","else","if"]
quotes = ["\"","\'","‘","’","“","”"]
finites = {
    "operator": ["=","+",">"],
    "separator": ["(",")",":"]
}
# Add quotes to the separator array in the dictionary, but also keep it in its own array
finites["separator"].extend(quotes)

class Keyword():
    def __init__(self):
        # Every keyword gets its own state
        self.curr_states = {}
        for kw in keywords:
            self.curr_states[kw] = ""
        self.new_state = ""
    def __call__(self, char, index):
        self.new_state = char
        self.index = index
        return self._run_all()
    def _run_kw(self, word):
        
        if self.curr_states[word] == "":
            if self.new_state == " ":
                self.curr_states[word] = " "
            elif self.new_state == word[0] and self.index == 0:
                self.curr_states[word] = word[0]
            return None
        
        
        if self.curr_states[word] == " " and (self.new_state == "\n" or self.new_state in finites["separator"]):
            self.__init__()
            return None
        state = " "
        for c in word:
            if self.curr_states[word] == state and self.new_state == c:
                self.curr_states[word] = c
                return None
            state = c
        if self.curr_states[word] == word[-1]:
            if self.new_state == " ":
                self.curr_states[word] = " "
            elif (self.new_state == "\n" or self.new_state in finites["separator"]):
                self.__init__()
            else:
                self.__init__()
                return None
            return "<keyword,{}>".format(word)
    def _run_all(self):
        for kw, state in self.curr_states.items():
            temp = self._run_kw(kw)
            if temp != None:
                return temp
keyword = Keyword()

def single_char_tokens(char, index):
    for key, val in finites.items():
        for i in val:
                if char == i:
                    return "<{},{}>".format(key,i)
    return None

States = Enum("States", "neither integer string ident")
class AlphaNum():
    def __init__(self):
        self.string = ""
        self.state = States.neither
    def __call__(self, char, index):
        if self.state == States.neither:
            if char.isdigit():
                self.string += char
                self.state = States.integer
                return None
            elif char.isalpha():
                self.string += char
                self.state = States.ident
                return None
            elif char in quotes:
                self.state = States.string
        elif self.state == States.integer:
            if char.isdigit():
                self.string += char
                return None
            elif char.isalpha():
                return self._print(States.ident, char)
            elif char in quotes:
                return self._print(States.string)
            else:
                return self._print(States.neither)
        elif self.state == States.ident:
            if char.isalpha() or char.isdigit():
                self.string += char
                return None
            elif char in quotes:
                return self._print(States.string)
            else:
                return self._print(States.neither)
        elif self.state == States.string:
            if char in quotes:
                return self._print(States.neither)
            else:
                self.string += char

    def _print(self, state, ch = ""):
        value = self.string
        self.string = ch
        if (self.state == States.integer) or (self.state == States.string):
            key = "literal"
        elif self.state == States.ident:
            key = "identifier"
        else:
            key = "error"

        self.state = state
        
        if (value not in keywords) or (key == "literal"):
            return "<{},{}>".format(key,value)
        else:
            return None
    
        
        
    
alpha_num = AlphaNum()


fsms = [keyword, alpha_num, single_char_tokens]


def tokenize(_line):
    line = _line + "\n"
    tokens = []
    for index, char in enumerate(line):
        for m in fsms:
            out = m(char, index)
            if out != None:
                tokens.append(out)
    return tokens