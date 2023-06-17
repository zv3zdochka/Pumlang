class SkipIterator:
    def __init__(self, iterator, n):
        self.iterator = iter(iterator)
        for _ in range(n):
            next(self.iterator)
        self.r()

    def r(self):
        return self.iterator

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)


class Compiler:
    def __init__(self, comp_liste, variables={}):
        self.cutter = comp_liste
        self.comp_list = iter(comp_liste)
        self.stack = []
        self.got_list = self.comp_list
        self.current = None
        self.previous = None
        self.lex_index = 0
        self.variables = variables  # name: [type, value]

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def handle_none_type_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError as e:
                if "'NoneType' object is not subscriptable" in str(e):
                    print(f"Tyring to use unknown variable {self.previous, self.current, self.get_next_tok()}")
                else:
                    raise e

        return wrapper
    def get_next_tok(self, cond='', n=0):
        if n != 0:
            try:
                n = int(n)
            except Exception:
                print('Strange_value_of_line_in_while')
        if n > 0:
            try:
                it = SkipIterator(self.cutter, n)
                self.got_list = it
            except:
                return '&'
        else:
            if cond:
                track = []
                while True:
                    try:
                        self.previous = self.current
                        out = next(self.got_list)
                        if out == ';':
                            continue
                        elif out in cond:
                            track.append(out)
                            return track
                        else:
                            track.append(out)
                    except StopIteration:
                        track.append('&')
                        return track
            else:
                while True:
                    try:
                        self.previous = self.current
                        out = next(self.got_list)
                        if out == ';':
                            continue
                        return out
                    except StopIteration:
                        return '&'
    @handle_none_type_error
    def compi(self):
        comparison_operators = ['<', '>', '<=', '>=', '==', '!=']
        logical_operators = ['and', 'or', 'not']
        math_operators = ['+', '-', '*', '/', '//', '%', '^']
        prep = False
        while True:
            self.current = self.get_next_tok()
            if self.current == '&':
                exit()
            elif self.current == '%revers%':
                if prep:
                    pass
                else:
                    return self.variables
            if self.current == 'input':
                var = self.stack.pop()
                inp = input()
                self.variables[var] = [type(inp), inp]
            elif self.current == 'print':
                var = self.stack.pop()
                if var in self.variables:
                    var = self.variables.get(var)[1]
                print(var)
            elif self.current == 'while':
                f_srt = self.stack.pop()[1:]
                cond = self.stack.pop()
                if cond == 'true':
                    self.current = self.get_next_tok(['%revers%'])

                    need_line = self.current[len(self.current) - 2][1:]

                    C = Compiler(self.current, variables=self.variables)
                    var = C.compi()
                    for i, j in var.items():
                        self.variables[i] = j

                    self.get_next_tok(n=need_line)
                else:
                    prep = True
                    self.get_next_tok(n=f_srt)
            elif self.current in ['int', 'float', 'str']:
                for i in self.stack:
                    self.variables[i] = [self.current, '']
            elif self.current == ':=':
                n_1 = self.stack.pop()
                n_2 = self.stack.pop()
                if n_1 in ['false', 'true'] or type(n_1) in [float, int] or self.is_number(n_1):
                    if n_1 in ['true', 'false']:
                        n_1 = bool
                    elif True:
                        try:
                            t_n_1 = type(int(n_1))
                            v_n_1 = int(n_1)
                        except Exception:
                            try:
                                t_n_1 = type(float(n_1))
                                v_n_1 = float(n_1)
                            except Exception:
                                print('Error value of variable')
                                exit()
                        self.variables[n_2] = [t_n_1, n_1]
                else:
                    v_n_1 = self.variables.get(n_1)
                    if v_n_1 is None:
                        print('Error value of variable')
                        exit()
                    else:
                        self.variables[n_2] = [v_n_1[0], v_n_1[1]]
            elif self.current == 'else':
                pass # костыль в жопе еще никому не повредил
            elif self.current in ['{', '}', '(', ')']:
                pass # тут в целом тоже
            elif self.current == 'if':
                f_srt = self.stack.pop()[1:]
                cond = self.stack.pop()
                if cond == 'true':
                    self.current = self.get_next_tok(['elif', 'else'])
                    go_line = self.current[len(self.current) - 2]
                    self.current.remove(go_line)

                    C = Compiler(self.current, variables=self.variables)
                    var = C.compi()
                    for i, j in var.items():
                        self.variables[i] = j
                    self.get_next_tok(n=f_srt)
                else:
                    self.get_next_tok(n=f_srt)
                    self.get_next_tok()


            elif self.current in math_operators:
                if self.current == '+':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 + val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == '-':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 - val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == '*':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 * val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == '/':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 / val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == '//':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 // val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == '%':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 % val_1

                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == '^':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 ** val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
            elif self.current in logical_operators:
                if self.current == 'and':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = bool(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = bool(self.variables.get(val_2)[1])

                    res = val_2 and val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == 'or':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = bool(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = bool(self.variables.get(val_2)[1])

                    res = val_2 or val_1
                    if res.is_integer():
                        res = int(res)
                        self.stack.append(res)
                    else:
                        self.stack.append(res)
                elif self.current == 'not':
                    val_1 = self.stack.pop()
                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = bool(self.variables.get(val_1)[1])

                    res = not val_1
                    self.stack.append(res)
            elif self.current in comparison_operators:
                if self.current == '<':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()

                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 < val_1
                    self.stack.append(str(res).lower())

                elif self.current == '>':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()

                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 > val_1
                    self.stack.append(str(res).lower())

                elif self.current == '<=':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()

                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 <= val_1
                    self.stack.append(str(res).lower())

                elif self.current == '>=':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()

                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 >= val_1
                    self.stack.append(str(res).lower())

                elif self.current == '==':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()

                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 == val_1
                    self.stack.append(str(res).lower())

                elif self.current == '!=':
                    val_1 = self.stack.pop()
                    val_2 = self.stack.pop()

                    try:
                        val_1 = float(val_1)
                    except Exception:
                        val_1 = float(self.variables.get(val_1)[1])

                    try:
                        val_2 = float(val_2)
                    except Exception:
                        val_2 = float(self.variables.get(val_2)[1])

                    res = val_2 != val_1
                    self.stack.append(str(res).lower())
            else:
                self.stack.append(self.current)
