import colorama


class Prn:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_char = ''
        self.line_number = 0
        self.r_len = 0
        self.queue = []
        self.stack = []

    def get_next_token(self, line_returner=False):
        token_list = []
        breaks = 0
        while True:
            try:
                out = next(self.tokens)
            except StopIteration:
                if line_returner:
                    return token_list
                else:
                    return '&'
            if line_returner:

                if out in ['if', 'elif', 'else']:
                    breaks += 1
                if out in ('{', ';', '}') and breaks == 0:
                    token_list.append(out)
                    return token_list
                elif out in ('{', ';', '}') and breaks != 0:
                    token_list.append(out)
                    breaks -= 1
                else:
                    if out == '$':
                        self.line_number += 1
                    else:
                        token_list.append(out)
            else:
                if out == "$":
                    self.line_number += 1
                    continue
                else:
                    return out

    @staticmethod
    def infix_to_postfix_for_expression(infix):
        quality = {"not": 3, "*": 2, "/": 2, "//": 2, "%": 2, "^": 2, "+": 1, "-": 1, ">": 0, ">=": 0, "<": 0, "<=": 0,
                   "==": 0,
                   "!=": 0, "and": -1, "or": -2}
        postfix = []
        stack = []
        tokens = infix

        for token in tokens:
            if token.isnumeric() or token.isalpha() and token not in ['and',
                                                                      'or'] or token == "true" or token == "false":
                postfix.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack[-1] != "(":
                    postfix.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != "(" and quality.get(token, -3) <= quality.get(stack[-1], -3):
                    postfix.append(stack.pop())
                stack.append(token)

        while stack:
            postfix.append(stack.pop())

        return postfix

    def infix_to_postfix(self):
        while self.current_char != '&':
            self.current_char = self.get_next_token()
            if self.current_char in ['{', '}']:
                continue
            elif self.current_char in ['int', 'bool', 'float']:
                self.queue.append(self.current_char)
                self.current_char = self.get_next_token()
                if not self.current_char.isalpha():
                    return (
                            colorama.Fore.RED + f'Expected variable name, but got {self.current_char} at line {self.line_number}')

                else:
                    self.queue.append(self.current_char)
                    self.current_char = self.get_next_token()
                if self.current_char == ',':
                    while self.current_char == ',':
                        self.current_char = self.get_next_token()
                        if self.current_char.isalpha():
                            self.queue.append(self.current_char)
                        else:
                            return (
                                    colorama.Fore.RED + f'Expected variable name, but got {self.current_char} at line {self.line_number}')
                        self.current_char = self.get_next_token()
                        if self.current_char == ',':
                            continue
                        elif self.current_char == ';':
                            break
                    if self.current_char == ';':
                        self.queue.reverse()
                        for i in self.queue:
                            self.stack.append(i)
                            self.queue = []
                        self.stack.append(';')
                elif self.current_char == ':=':
                    self.queue.append(self.current_char)
                elif self.current_char == ';':
                    self.queue.reverse()
                    for i in self.queue:
                        self.stack.append(i)
                    self.queue = []
                    self.stack.append(';')
                else:
                    return (
                            colorama.Fore.RED + f'Expected "," or ":=" or ";", but got {self.current_char} at line {self.line_number}')

            elif self.current_char == 'input':
                self.current_char = self.get_next_token()
                self.current_char = self.get_next_token()
                if self.current_char.isalpha():
                    self.stack.append(self.current_char)
                    self.stack.append('input')
                    self.stack.append(';')
                else:
                    return (
                            colorama.Fore.RED + f'Expected variable name, but got {self.current_char} at line {self.line_number}')
                self.current_char = self.get_next_token()


            elif self.current_char == 'print':
                self.current_char = self.get_next_token()
                q = self.get_next_token(True)
                if q[len(q) - 2] != ')':
                    return (
                            colorama.Fore.RED + f'Expected ")", but got {self.current_char} at line {self.line_number}')
                else:
                    q.pop(len(q) - 2)
                    post = self.infix_to_postfix_for_expression(q)
                    post.remove(';')
                    for i in post:
                        self.stack.append(i)
                    self.stack.append('print')
                    self.stack.append(';')


            elif self.current_char == 'while':
                self.current_char = self.get_next_token()
                q = self.get_next_token(True)
                if q[len(q) - 2] != ')':
                    return (
                            colorama.Fore.RED + f'Expected ")", but got {self.current_char} at line {self.line_number}')
                else:
                    q.pop(len(q) - 2)
                    rever_line = len(self.stack)
                    post = self.infix_to_postfix_for_expression(q)
                    post.remove('{')
                    post.remove('}')
                    for i in post:
                        self.stack.append(i)
                    except_len = len(self.stack)
                    self.stack.append('while')
                    line = self.get_next_token(True)
                    n_p = Prn(line)
                    r_line = n_p.infix_to_postfix()[0]
                    self.get_next_token()
                    for i in r_line:
                        if i == ';':
                            continue
                        self.stack.append(i)
                    self.stack.append(rever_line)
                    self.stack.append('%revers%')
                    self.stack.append(';')
                    self.stack.insert(except_len, "'" + str(len(self.stack) + 1))


            elif self.current_char == 'if':
                self.current_char = self.get_next_token()
                q = self.get_next_token(True)

                if q[len(q) - 2] != ')':
                    return (
                            colorama.Fore.RED + f'Expected ")", but got {self.current_char} at line {self.line_number}')
                else:
                    q.pop(len(q) - 2)

                    post = self.infix_to_postfix_for_expression(q)
                    post.remove('{')
                    for i in post:
                        self.stack.append(i)
                    rever_line = len(self.stack)
                    self.stack.append('if')
                    line = self.get_next_token(True)
                    print(line)
                    n_p = Prn(line)
                    r_line = n_p.infix_to_postfix()
                    self.get_next_token()
                    for i in r_line:
                        if i == ';':
                            continue
                        self.stack.append(i)
                    self.stack.append(';')
                    self.current_char = self.get_next_token()
                    self.stack.insert(rever_line, "'" + str(len(self.stack) + 1))

                    if self.current_char == 'elif':
                        self.current_char = self.get_next_token()
                        q = self.get_next_token(True)
                        if q[len(q) - 2] != ')':
                            return (
                                    colorama.Fore.RED + f'Expected ")", but got {self.current_char} at line {self.line_number}')
                        else:
                            q.pop(len(q) - 2)
                            rever_line = len(self.stack)
                            post = self.infix_to_postfix_for_expression(q)
                            post.remove('{')
                            post.remove('}')
                            for i in post:
                                self.stack.append(i)
                            self.stack.append('elif')
                            line = self.get_next_token(True)
                            n_p = Prn(line)
                            r_line = n_p.infix_to_postfix()[0]
                            self.get_next_token()
                            for i in r_line:
                                if i == ';':
                                    continue
                                self.stack.append(i)
                            self.stack.append(';')

                            self.current_char = self.get_next_token()
                            self.stack.insert(rever_line, "'" + str(len(self.stack) + 1))

                            if self.current_char == 'else':
                                self.stack.append('else')
                                self.current_char = self.get_next_token()
                                line = self.get_next_token(True)
                                n_p = Prn(line)
                                r_line = n_p.infix_to_postfix()[0]
                                self.get_next_token()
                                for i in r_line:
                                    if i == ';':
                                        continue
                                    self.stack.append(i)
                                self.stack.append(';')

                    elif self.current_char == 'else':
                        self.stack.append('else')
                        self.current_char = self.get_next_token()
                        line = self.get_next_token(True)
                        n_p = Prn(line)
                        r_line = n_p.infix_to_postfix()[0]
                        self.get_next_token()
                        for i in r_line:
                            if i == ';':
                                continue
                            self.stack.append(i)
                        self.stack.append(';')









            elif self.current_char.isalpha():
                cur = self.current_char
                infix_line = self.get_next_token(True)
                infix_line.insert(0, cur)
                postfix = self.infix_to_postfix_for_expression(infix_line)
                for i in postfix:
                    self.stack.append(i)
        return self.stack


P = Prn(
    ['{', '$', '$', 'if', '(', 'a', '>=', '10', ')', '$', '{', '$', 'if', '(', 'a', '%', '2', '==', '0', ')', '$', '{',
     '$', 'print', '(', '1', ')', ';', '$', '}', '$', '$', 'else', '{', '$', 'print', '(', '2', ')', ';', '$', '}', '$',
     '}', '$', '$', 'else', '{', '$', 'print', '(', '3', ')', ';', '$', '}', '$', '}'])
print(P.infix_to_postfix())
