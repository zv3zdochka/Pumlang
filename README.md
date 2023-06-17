
 # PumLang

This guide contains information about the PumLang project - the PumLang programming language interpreter. This was a tutorial project, so I'll try to add some comments in the code and describe what works and how it works as much as possible.

# Description

PumLang is a programming language that implements the following requirements:

- Variables: The language supports variables to which you can assign values and then use those values in the program.
- Strict typing: Variables in PumLang have strict typing. When declaring a variable, the programmer must specify the data type it will store.
- Data types: The language supports integers, real numbers and boolean values (true and false).
- Conditional statement: A conditional statement is supported, which allows you to execute a block of code if a certain condition is met.
- Loop statement: A loop statement is supported, which allows you to execute a block of code in a loop as long as some condition is met.
- Error handling: If there is a syntax error in the program, the interpreter should report it by specifying the line where it occurred and briefly describing its nature.
- Entering a variable value: The language allows the user to enter variable values that are read from the keyboard using the `input()` function in Python.
- Display expression values on the screen: The language provides a function for displaying expression values on the screen.

# Architecture

The architecture of the PumLang interpreter follows the following basic steps:

1. Lexical analysis: At this stage, the source code of the program is broken down into tokens such as operators, keywords, identifiers, etc. The lexical analyzer processes the string and creates a list of tokens.
2. Syntax analysis: The list of tokens is analyzed to check the syntactic correctness of the program. The recursive descent method is used to build a syntax tree or other form of internal program representation.
3. program execution: The interpreter executes the program using the internal representation. This includes working with the stack to store values and performing operations according to the logic of the PumLang language.

# Pumlang grammar
```python
P -> B | &
B -> {S [;S]^}
S -> [int | bool | float] I [,I]^ | [int | bool | float] I := E| I := E | if (E) B [else B] | while (E) B | input(I) | print(E)
E -> E1 [[> | < | = | !=] E1]
E1 -> T [[+ | - | or] T]^
T -> F [[* | / | % | // | and] F]^
F -> I | N | L | not F | (E)
L -> true | false
I -> C[C]^
N -> R[.R]
R -> D[D]^
C -> a | b | ... | z
D -> 0 | 1 | ... | 9

```


Let's try to understand what is written. This grammar contains two types of entities: terminals, such as int, bool, a, etc., and non-terminals, denoted by capital letters. Under each nonterminal symbol is hidden its output rule. The names of nonterminal symbols in this grammar are not chosen by chance:
The vertical slash | means to choose one of the options, [] means that everything inside the brackets is optional, i.e. it may not exist, the notation []^ means that what is written in brackets may be repeated several times (possibly 0).
Let's look at some of the rules in a little more detail.


Let's break down each point in the grammar of the language:

1. P (Programm) -> B&
   - The program consists of an instruction block B, which may be followed by an "&", which works like exit() in python.

2. B (Block) -> {S [;S]^}
   - The instruction block is enclosed in curly braces "{}".
   - A block contains one or more S instructions separated by ";".
   - Instructions may be repeated zero or more times.

3. S (Statement) -> [int | bool | float] I [,I]^ | [int | bool | float] I := E| I := E | if (E) B [else B] | while (E) B | input(I) | print(E)
   - The instruction may be one of the following:
     - A variable declaration of type "int", "bool" or "float" followed by identifier I. There can be one or more declarations, separated by a comma.
     - Assigning the value of expression E to a variable named I.
     - Declaration of a variable with assignment of value and data type. int hello := 5. 
     - The conditional "if" statement, which tests expression E. It is followed by a block of instructions B. A block of instructions for the "else" case may also be specified.
     - The "while" loop, which is executed as long as the condition of expression E is true. It is followed by a block of instructions B.
     - An "input" instruction that reads a value from the console and assigns it to a variable named I.
     - The "print" instruction, which prints the value of expression E to the screen.

4. E (Expression) -> E1 [[> | < | == | != >= <=] E1]
   - An expression can be a comparison of two E1 expressions using the comparison operators ">" (greater than), "<" (less than), ">=" (greater than or equal to), "<=" (less than or equal to), "=" (equal) or "!=" (not equal).

5. E1 (Expression1) -> T [[+ | - | or] T]^
   - An expression can contain one or more summands T, which can be added (+), subtracted (-) or combined by the logical operator "or".

6. T (Term) -> F [[* | / | % | // | and] F]^
   - An expression can contain one or more multipliers F, which can be multiplied (*), divided (/), taken the remainder of division (%), integer divided (//) or combined by the logical operator "and".

7. F (Factor) -> I | N | L | not F | (E)
   - An expression can be an identifier I, a number N, a logical value L, a logical operation "not" from another expression F, or an expression in parentheses (E).

8. L (Boolean literal) -> true | false
   - The logical value can be either "true" (true) or "false" (false).

9. I (Identifier) -> C[C]^
   - The identifier begins with a C character, which may be followed by a zero or more C characters.

10. N (Number) -> R[.R]
    - A number consists of an integer part R, which may be followed by a decimal part separated by ".

11. R (Digit) -> D[D]^
    - A number or an integer part of a number consists of one or more digits D.

12. C (Letter) -> a | b | ... | z
    - The identifier characters can be small Latin letters from "a" to "z".

13. D (Digit) -> 0 | 1 | ... | 9
    - The numbers are represented by symbols from "0" to "9".


# Interpretation

No special libraries other than sys were used when writing the code, and that was to run everything through the command line.
Suppose we want to write a program that outputs the factorial of a number in Pumlang. Knowing the grammar of the language we sketched this code.

```python
{
    int n, s;
    input(n);
    s := 1;
    while (n > 1) {
        s := s * n;
        n := n - 1
    };
    print(s);
}
```


# Running your own code

Initially, it is planned that the code written in the Pumlang language will be run through the command line. The file which contains the program written in the Pumlang language is called main.plg. The main file in the project, which we will refer to in the command line is called pumlang.py. 

```bash.

C:/Pumlang/python pumlang.py main.plg
```

# Lexical analysis. 

The lexical analysis stage is one of the first steps in processing and analyzing source code in computer programs. It is the process of parsing source code into a sequence of tokens, or tokens, which are the minimal semantic units in a programming language. The purpose of lexical analysis is to break down the source code into simpler elements that can be more easily processed and analyzed at higher levels of compilation or program interpretation. This step is an important part of the software development process and the basis for further code analysis and execution. Here is a general sequence of steps that are usually included in the lexical analysis step:


### 1. Tokenization
Source code is broken down into individual characters and character sequences called tokens. Tokens can represent keywords, variable identifiers, operators, numbers, strings, and other programming language elements. Spaces and comments are usually ignored.

```bash.
[ "{", "\n", " ", "int", " ", "n", ", ", " ", "s", ";", "\n", " ", "input", "(", " ", "n", ")", ";", "\n", " ", "s", ", ":=", " ", "1", ";", "\n", " ", "while", " ", "(", " ", "n", " ", ">", " ", "0", " ", ")", " ", "{", "\n", " ", "s", " ":=", " ", "s", " ", "*", " ", "n", ";", "\n", " ", "n", " ", ":=", " ", "n", " ", "-", " ", "1", ";", "\n", ", "}", ", ";", "\n", " ", "print", "(", ", "s", ", ")", ";" ,"\n", " ", "}", "

```

### 2. Deleting non-significant characters
The lexical analyzer removes non-significant characters, such as spaces, tabs and line feeds, which do not affect the meaning of the program.

```bash.
[{, int, n, ',', s, ;, input, (, n, ), ;, s, :=, 1, ;, while, (, n, >, 0, ), {, s, :=, s, *, n, ;, n, :=, n, -, 1, ;, }, ;, print, (, s, ), ;, }]


```

### 3. Classification of tokens
Each token is classified according to its type. For example, keywords, operators and identifiers can be classified into different categories.

- `{`, `}`: `LexBraceOpen`, `LexBraceClose`
- `(`, `)`: `LexBktOpen`, `LexBktClose`
- `,`: `LexComma
- `;`: `LexSemicolon
- `&`: `LexEnd
- `int`, `float`, `bool`: `LexType`
- Identifiers (e.g. `n`, `s`): `LexId`.
- Integer constants (e.g. `1`): `LexInt`.
- Real constants (not in this token list)
- Boolean constants (not on this token list)
- `:=`: `LexAssign'
- `input`: `LexInput`
- `print`: `LexPrint`
- `if`: `LexIf'
- `else`: `LexElse`
- `while`: `LexWhile`
- `and`: `LexAnd`
- `or`: `LexOr`
- `not`: `LexNot`
- Binary operations (not on this list of tokens)

### 4. Error handling
The lexical analyzer can detect and handle errors in code, such as invalid characters, invalid token combinations and other language syntax violations.

```python
If tokens.count('{') != tokens.count('}') or tokens.count(') != tokens.count(')')
    print('Program must have an equal number of opening and closing brackets of all types')
    exit(-1)
elif tokens[0] == '{' and tokens[len(tokens) - 1] == '}':
    return tokens
else:
    print('Program must be in curly brackets: {your code}')
    exit(-1)

```

In this code snippet, we make sure that the number of opening and closing parentheses of all kinds is the same and that the program itself is inside the {} parentheses. The result of lexical analysis is a sequence of tokens or tokens, which is passed to the next processing step, such as parsing.

```python
[{, int, n, ',', s, ;, input, (, n, ), ;, s, :=, 1, ;, while, (, n, >, 0, ), {, s, :=, s, *, n, ;, n, :=, n, -, 1, ;, }, ;, print, (, s, ), ;, }]

```


# Syntactic analysis 

Syntax analysis is the process of analyzing and parsing program code to determine its structure and compliance with the syntax rules of a particular programming language. A parser (also known as a parser) uses grammatical rules defined for a language to determine if the code is written correctly and what operations are performed in the code.
In our case, we use the recursive descent method for parsing code, based on our grammar. That is, the program will jump between states by skipping through the code, and in case of inconsistency, it will generate an error. 

A simple transition between states at the start of the program is implemented here.

```python
   def P(self):
       self.state = "B"
       self.B()
       return
```

And here the transition from state B to state S is implemented. At the same time we count the number of brackets to catch the error before the main parsing, which will speed up the already fast program. We also check for ";" after each line.

```python
   def B(self):
       self.current = self.get_next_elem()
       self.match('{')
       self.current = self.get_next_elem()
       self.state = "S"
       self.S()
       self.state = 'B'
       if self.current != ';' and self.previous not in ['{', '}']:
           self.error(
               f "Expected ; but got {'nothing' if self.current in ['{', '}', '&', ';'] else self.current}")
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
                   f "Expected ; but got {'nothing' if self.current in ['{', '}', '&', ';'] else self.current}")

```
So having parsed through all the code and not getting an error we can move on to the next step.

# Program Execution

The execution of the program will be divided into two stages. 

### 1. Translation to postfix notation

Translation to Polish notation is done in the file Polish_reversed_notation. Which is started from the file pumlang.py. The usual algorithm for translation into Polish notation is used, you can read about it here https://habr.com/ru/articles/100869/, but also the algorithm has been modified for such operators as int, while, etc. 
As a result, we get the following list of elements, ready to be executed, after translating it into postfix notation (aka Polish notation).
 
```python
 
 [n, s, int, n, input, 1, s, :=, 1, n, >, 25, while, s, n, *, s, :=, n, 1, -, n, :=, 8, goto, s, print]

 ```
 
Note 8, 25, and goto, which were not in the list of tokens. These are addresses and the jump function, respectively (in this case, by address we mean the number of the element in the given list). When goto is encountered, the interpreter will continue the computation from the number of the element to the left of goto in this chain. 

### 2. Internal program execution

Now, having a list of elements in postfix notation, executing this program is a pleasure! Simply, when we get some elements, we put them on the stack, and if we encounter any operator, we get a certain number of elements. 
Here is an example of adding two numbers. 

```python
def evaluate(self):
        o1 = self.stack.pop()
        o2 = self.stack.pop()
        res = o1.value + o2.value
        if isinstance(res, int):
            res = PrnInt(res)
        else:
            res = PrnFloat(res)
        self.stack.push(res)
```

In the file Compile.py everything is also implemented taking into account the variability of data types, for example in order to make arithmetic operations with two numbers 1.4 of type float and 4 of type int. 
Also implemented the possibility of nesting conditions, it can be seen in the tests. 

## Program testing

After a long and painful debug, we can start testing. We will have several tests, which are the first programs any programmer writes. 

### Test 1

Output the entered number

```python
{
    input(a);
    print(a);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 3
3
```
Great first test was successful, as we can see everything works.


### Test 2 

The program gets two numbers (one in each line). Output the sum of the numbers to the screen.

```python
{
    input(a);
    input(b);
    print(a + b);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 3
>>> 4
7
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 234.24234
>>> 6345345
6345579.24234
```
The second test also works, even with non-integer numbers. 


### Test 3

The length of the Moscow Ring Road is 109 kilometers. Biker Vasya starts from kilometer zero of the Moscow Ring Road and rides at speed v kilometers per hour. At what point will he stop after t hours?
The two lines enter v and t.

```python
{
    input(a);
    input(b);
    print((a * b) % 109);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 38
>>> 9
15
```
The third test works. 


### Test 4

Enter two numbers (one on each line). Output the least common divisor of these numbers.

```python
{
    int temp := 0;
    input(a);
    input(b);
    while (b != 0)
    {
        temp := b;
        b := a % b;
        a := temp;
    }
    print(a);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 884
>>> 153
17
```
```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 2364826487326874.2424242
>>> 28423742.24224234 
3.725290298461914e-09
```
```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 3246726482648723648723642746283764
>>> 4824632848273648732648726424628424
576460752303423488
```

The fourth test passed even with huge and fractional numbers. 


### Test 5

Enter a natural number N. Output the factorial of N.

```python
{
    input(a);
    int fac := 1;
    if (a == 0)
    {
        print(1);
        &
    }
    else
    {
        while (a > 0)
        {
            fac := fac * a;
            a := a - 1;
        }
    }
    print(fac);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 4
24
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 123
12146304367025331529099877131181532511825408382397052669269085336752145805972232396989773798415332323726739178998923342612698329488403802367592326091522384520570604998598324075751895482385020694083942744064
```
The fifth test also works, and relatively quickly. 


### Test 5
Enter N. Output the Nth Fibonacci number.

```python
{
    int a, b, i, c;
    input(n);
    a := 0;
    b := 1;
    i := 1;
    while (i < n)
    {
        c := a + b;
        a := b;
        b := c;
        i := i + 1;
    }
    print(b);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 3
2
```
```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 123
22698374052006868279099392

```
The fifth test also passed. 


### Test 6

Now let's try to catch errors and see how the interpreter reacts to them

```python
{
    input(a)
    input(b);
    print((a * b) % 109);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
Invalid syntax error at line 2: input .
Expected ; but got input
```

```python
{
    iput(a);
    input(b);
    print((a * b) % 109);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
Invalid syntax error at line 1: iput .
Attempt to perform an undeclared variable operation
```

As we can see the errors are perfectly handled. 

### Boss fight

Let's try to deduce the nth prime number

```python
{
    int i, a, j, d, k;
    input(n);
    i := 0
    a := 0;
    j := 2;
    while (j > 0)
    {
        d := 0;
        k := 1;
        while (k < j + 1)
        {
            if (j % k) == 0
            {
                d := d + 1;
            }
            k := k + 1;
        }
        if (d == 2)
        {
            i := i + 1;
            a := j;
        }
        if (j == n)
        {
            j := j - 1;
        }
        else
        {
            j := j + 1;
        }
    }
print(a);
}
```

```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 3
5
```
It was hard but it works, let's try something heavier. 
```python
C:\Users\PumLang> python pumlang.py main.plg
>>> 1000000
#five years later
15485863
```
# Conclusion

And now we have finished writing our python interpreter. Yes, even if it does not have some advantages over python due to poor optimization and the whole idea of writing the interpreter in python. However, while writing this interpreter all the aspects of the writing were explained in details together with the theory and code snippets, so as an educational case this project will do just fine. If you have any questions you can write to mai.batsiev.oleg@gmail.com 
