import sys
from Polish_reversed_notation import Prn
from Compile import Compiler


class Lexer:
    def __init__(self, plg):
        self.text = self.make_lexemes(plg)

    @staticmethod
    def make_lexemes(code):
        flag = False
        tokens = []
        current_token = ''
        is_comment = False
        for i, char in enumerate(code):
            if flag:
                flag = False
                continue

            if char == '#' and (i == 0 or code[i - 1] in ['\n', ' ']):
                is_comment = True
            if char == '\n':
                is_comment = False
                tokens.append('$')
            if is_comment:
                continue
            if char in ['{', '}', ',', ';', '(', ')', ':', '=', '>', '<', '-', '*', '+', '!']:
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
                if char == ':' and i < len(code) - 1 and code[i + 1] == '=':
                    tokens.append(':=')
                    flag = True
                elif char == '>' and i < len(code) - 1 and code[i + 1] == '=':
                    tokens.append('>=')
                    flag = True
                elif char == '<' and i < len(code) - 1 and code[i + 1] == '=':
                    tokens.append('<=')
                    flag = True
                elif char == '=' and i < len(code) - 1 and code[i + 1] == '=':
                    tokens.append('==')
                    flag = True
                elif char == '!' and i < len(code) - 1 and code[i + 1] == '=':
                    tokens.append('!=')
                    flag = True
                else:
                    tokens.append(char)
            elif char == '/' and i < len(code) - 1 and code[i + 1] == '/':
                tokens.append('//')
                flag = True
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            else:
                current_token += char
        if current_token:
            tokens.append(current_token)
        tokens.reverse()
        for i in tokens:
            if i == '$':
                tokens.remove(i)
            else:
                break
        tokens.reverse()

        if tokens.count('{') != tokens.count('}') or tokens.count('(') != tokens.count(')'):
            print('Program must have an equal number of opening and closing brackets of all types')
            exit(-1)
        elif tokens[0] == '{' and tokens[len(tokens) - 1] == '}':
            return tokens

        else:
            print('Program must be in curly brackets: {your code}')
            exit(-1)

    @staticmethod
    def remove_brackets(lst):
        return [x for x in lst if x not in ['(', ')', '{', '}', ';']]
    def parse(self):
        # print(self.text)  # print list of lexemes

        class Parser:
            def __init__(self, tokens):
                self.tokens = iter(tokens)
                self.lend = len(tokens)
                self.r_len = 0
                self.current = None
                self.index = 0
                self.line_number = 0
                self.state = ''
                self.mem = set()
                self.curly_brace = 0
                self.array = []
                self.previous = None




            def get_next_elem(self):
                while True:
                    try:
                        self.previous = self.current
                        out = next(self.tokens)
                    except Exception:
                        return '&'
                    if out == "$":
                        self.line_number += 1
                        self.r_len += 1
                        continue
                    else:
                        self.r_len += 1
                        # print(out)  # print current lexeme
                        self.array.append(out)
                        return out

            def error(self, description):
                print(
                    f"Invalid syntax error at line {self.line_number}: \033[4m{' ' + self.current + ' '}\033[0m." + "\n" + f"{description}")
                exit(-1)

            def match(self, expected_token_type):
                if self.current == expected_token_type:
                    return
                else:
                    self.error(
                        f"Expected {expected_token_type} but got {'nothing' if self.current in ['{', '}', '&', ';'] else self.current}", )
                    exit()

            def parse(self):
                if self.state == "":
                    self.state = 'P'
                    self.P()
                    return

            def P(self):
                self.state = "B"
                self.B()
                return

            def B(self):
                self.current = self.get_next_elem()
                self.match('{')
                self.current = self.get_next_elem()
                self.state = "S"
                self.S()
                self.state = 'B'
                if self.current != ';' and self.previous not in ['{', '}']:
                    self.error(
                        f"Expected ; but got {'nothing' if self.current in ['{', '}', '&', ';'] else self.current}")
                while True:
                    self.current = self.get_next_elem()
                    if self.current == '}':
                        self.current = self.get_next_elem()
                        if self.current == '&':
                            return
                        else:
                            return
                    self.state = 'S'
                    self.S()
                    if self.current == '}' or '{':
                        return
                    elif self.current == ';':
                        continue
                    else:
                        self.error(
                            f"Expected ; but got {'nothing' if self.current in ['{', '}', '&', ';'] else self.current}")

            def S(self):
                if self.current == '&':
                    return
                if self.current == ';':
                    return
                if self.current in ['{', '}']:
                    return
                elif self.current in ['int', 'bool', 'float']:  # add str
                    names = []
                    self.state = "I"
                    self.current = self.get_next_elem()
                    self.I()
                    if self.current in self.mem:
                        self.error(
                            'Variable with the same name have already used before')
                    names.append(self.current)
                    self.state = 'S'
                    self.current = self.get_next_elem()
                    if self.current == ':=':
                        self.state = 'E'
                        self.current = self.get_next_elem()
                        self.E()
                        self.state = 'S'
                    elif self.current == ',':
                        while True:
                            if self.current == ',':
                                self.current = self.get_next_elem()
                                self.state = "I"
                                self.I()
                                names.append(self.current)
                                self.state = 'S'
                                self.current = self.get_next_elem()
                            elif self.current == ';':
                                for i in names:
                                    self.mem.add(i)
                                names.clear()
                                break
                            else:
                                break
                    for i in names:
                        self.mem.add(i)
                    names.clear()

                elif self.current == 'if':
                    self.match('if')
                    self.current = self.get_next_elem()
                    self.match('(')
                    self.state = 'E'
                    self.current = self.get_next_elem()
                    self.E()
                    self.state = 'S'
                    self.match(')')
                    self.state = 'B'
                    self.B()
                    self.state = 'S'
                    if self.current == 'elif':
                        self.match('elif')
                        self.current = self.get_next_elem()
                        self.match('(')
                        self.state = 'E'
                        self.current = self.get_next_elem()
                        self.E()
                        self.state = 'S'
                        self.match(')')
                        self.state = 'B'
                        self.B()
                        self.state = 'S'
                        if self.current == 'else':
                            self.match('else')
                            self.state = 'B'
                            self.B()
                            self.state = 'S'
                            self.S()
                    elif self.current == 'else':
                        self.match('else')
                        self.state = 'B'
                        self.B()
                        self.state = 'S'
                        self.S()


                elif self.current == 'while':
                    self.match('while')
                    self.current = self.get_next_elem()
                    self.match('(')
                    self.current = self.get_next_elem()
                    self.state = 'E'
                    self.E()
                    self.state = 'S'

                    self.match(')')

                    self.state = 'B'
                    self.B()
                    self.state = 'S'

                elif self.current == 'input':
                    self.current = self.get_next_elem()
                    self.match('(')
                    self.current = self.get_next_elem()
                    self.state = 'I'
                    self.I()
                    self.current = self.get_next_elem()
                    self.match(')')
                    self.current = self.get_next_elem()

                elif self.current == 'print':
                    self.current = self.get_next_elem()
                    self.match('(')
                    self.current = self.get_next_elem()
                    self.state = 'E'
                    self.E()
                    self.state = 'S'
                    self.match(')')
                    self.current = self.get_next_elem()

                # elif self.current == 'func':
                #     pass

                elif type(self.current) is str:
                    self.state = 'I'
                    self.I()
                    if self.current not in self.mem:
                        self.error('Attempt to perform an undeclared variable operation')
                    self.current = self.get_next_elem()
                    self.match(':=')
                    self.current = self.get_next_elem()
                    self.E()
                    self.state = 'S'


                else:
                    self.error(f"Expected any construction but got {self.current}")

            def E(self):
                self.state = 'E1'
                self.E1()
                self.state = 'E'
                if self.current in ['>', '<', '=', '!=', '==', '>=', '<=']:
                    self.match(self.current)
                    self.current = self.get_next_elem()
                    self.E1()
                    self.state = 'E'

            def E1(self):
                self.state = "T"
                self.T()
                self.state = 'E1'
                while self.current in ['+', '-', 'or']:
                    self.match(self.current)
                    self.current = self.get_next_elem()
                    self.state = 'T'
                    self.T()

            def T(self):
                self.state = 'F'
                self.F()
                self.state = 'T'
                while self.current in ['*', '/', '%', '//', 'and', '**', '^']:
                    self.match(self.current)
                    self.current = self.get_next_elem()
                    self.F()
                    self.state = 'T'

            def F(self):
                if self.current in ['false', 'true']:
                    self.state = 'L'
                    self.L()
                    self.state = 'F'
                    return
                elif self.current.isalpha():
                    self.state = 'I'
                    self.I()
                    self.state = 'F'
                    self.current = self.get_next_elem()
                    return

                try:
                    float(self.current)
                    self.state = 'N'
                    self.N()
                    self.state = 'F'
                    return
                except Exception:
                    pass
                if self.current == 'not':
                    self.match('not')
                    self.state = 'F'
                    self.current = self.get_next_elem()
                    self.F()
                    self.current = self.get_next_elem()
                elif self.current == '(':
                    self.match('(')
                    self.state = 'E'
                    self.current = self.get_next_elem()
                    self.E()
                    self.match(')')
                    self.current = self.get_next_elem()
                else:
                    self.error(f"Expected any value or instruction but got {self.current}")

            def L(self):
                if self.current == 'true':
                    self.match('true')
                    self.current = self.get_next_elem()
                elif self.current == 'false':
                    self.match('false')
                    self.current = self.get_next_elem()

            def I(self):
                self.state = 'C'
                self.C()
                self.state = 'I'

            def N(self):
                self.state = 'R'
                self.R()
                self.state = 'N'

            def R(self):
                self.state = 'D'
                self.D()
                self.state = 'R'

            def C(self):
                if self.current.isalpha():
                    self.match(self.current)
                else:
                    self.error(f"Expected string variable name but got {self.current}")

            def D(self):
                try:
                    float(self.current)
                    self.match(self.current)
                    self.current = self.get_next_elem()
                except Exception:
                    self.error(f"Expected digit but got {self.current}")

        prs = Parser(self.text)
        prs.parse()

        prn = Prn(self.text)
        pol_not_de = prn.infix_to_postfix()

        #  pol_not = self.remove_brackets(pol_not_de)
        c = Compiler(pol_not_de)
        c.compi()


# if __name__ == "__main__":
#     inp_t = input()
#     L = Lexer(inp_t)
#     L.parse()
file_name = sys.argv[1]
with open(file_name, 'r', encoding='UTF-8') as m_file:
    inp_t = m_file.read()
    L = Lexer(inp_t)
    L.parse()
