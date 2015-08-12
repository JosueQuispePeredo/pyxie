#
# Copyright 2015 Michael Sparks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#START
"""
## Pyxie -- A Little Python to C++ Compiler

### What job does / will this do?

The aim of this project is to allow a adults and children to write code in a
familiar high level language that can then be compiled to run on an arbitrary
embedded system - that is devices with very low power CPUs and very little memory.
(ie devices too small to host a python interpreter/runtime) 

It's pre-alpha at the moment.

It will be useful in supporting things like the The Scout Association's "Digital
Maker" badge. That's a fair way off though.


### Show me something you CAN compile

Currently it can compile very very simple types of python program
that looks like this into an equivalent (simple) C++ program.

Example program:

    age = 10
    new_age = 10 +1
    new_age_too = age + 1
    new_age_three = age + new_age_too
    foo = "Hello"
    bar = "World"
    foobar = foo + bar

    print 10-1-2,7
    print 1+2*3*4-5/7,25
    print age, new_age, new_age_too
    print foo, bar, foobar

    countdown = 2147483647
    print "COUNTING DOWN"
    while countdown:
        countdown = countdown - 1

    print "BLASTOFF"

Example results:

    #include <iostream>
    #include <string>

    using namespace std;

    int main(int argc, char *argv[])
    {
        int age;
        string bar;
        int countdown;
        string foo;
        string foobar;
        int new_age;
        int new_age_three;
        int new_age_too;

        age = 10;
        new_age = (10+1);
        new_age_too = (age+1);
        new_age_three = (age+new_age_too);
        foo = "Hello";
        bar = "World";
        foobar = (foo+bar);
        cout << ((10-1)-2) << " " << 7 << endl;
        cout << ((1+((2*3)*4))-(5/7)) << " " << 25 << endl;
        cout << age << " " << new_age << " " << new_age_too << endl;
        cout << foo << " " << bar << " " << foobar << endl;
        countdown = 2147483647;
        cout << "COUNTING DOWN" << endl;
        while(countdown) {
            countdown = (countdown-1);
        };
        cout << "BLASTOFF" << endl;
        return 0;
    }


### What does it do?

Currently:

- Recognise simple sequential python programs with simple statements
- Can handle basic conditionals and while loops
- Custom includes, and function calls to C/C++ functions (within limits)
- Parse those to an AST
- Can represent equivalent C programs using a concrete C representation (CST)
- Can translate the AST to the CST and then generate C++ code from the CST

Python structural things it supports:

 - While loop statements
 - Comparisons
 - If/elif/elif/else statements
 - For loops - specific for X in range(Y)
 - Function calls into libraries that we link with

This is close to allowing actually useful programs now.

It's a starting point, not the end point. For that, take a look at the language spec.

Pyxie is intended to be a simple Python to C++ compiler, with a target of
compiling python code such that it can run on a microcontroller - like
Arduino, MSP430 or ARM mbed type devices.

The name is a play on words. Specifically, Python to C++ - can be py2cc or
pycc.  If you try pronouncing "pycc" it can be "pic", "py cc" or pyc-c".
The final one leads to Pixie.

This is unlikely to ever be a completely general python to C++ compiler - if
you're after than look at Shed Skin, or things like Cython, Pyrex, and PyPy.
(in terms of diminishing similarity) The difference this project has from
those is that this project assumes a very small target device.  Something
along the lines of an Atmega 8A, Atmega 328 or more capable.

Why not micropython? Micropython is **ace** . If your device is large enough to
support the micropython runtime, use it! The aim of this is on the really small
microcontrollers- the ones too small to even support micropython - like
an MSP430, or an Atmega 8A or similarly tiny MCU.


In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.


Why not micropython? Micropython is **ace** . If your device is large enough to
support the micropython runtime, use it! The aim of this is on the really small
microcontrollers- the ones too small to even support micropython - like
an MSP430, or an Atmega 8A or similarly tiny MCU.

In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.


## Status Overview

For the impatient: this probably does **NOT** do what you want, **yet**. <br>

High level view of support:

* Supports variables, sequence, and assignment
* while loops controlled by expressions, possibly involving variables
* while loops can contain break/continue which allows "if" style functionality
* Also have basic conditional operators like "==", "!=", etc.
* Ability to pull in C++ includes on standard paths

This means we can almost start writing useful programs, but in particular
can start creating simplistic benchmarks for measuring run speed. It IS
getting there however, and feedback, usecases, devices very welcome.


## Influences

Many moons ago, I made a generic language parser which I called SWP (semantic
 whitespace parser), or Gloop.

* <https://github.com/sparkslabs/minisnips/tree/master/SWP>
* <http://www.slideshare.net/kamaelian/swp-a-generic-language-parser>

It was an experiment to see if you could write a parser that had no keywords,
or similar, in a completely test driven fashion. ie a bit like a parser for a
Lisp like language that would look like python or ruby. It turns out that you
can and there's lots of interesting things that arise if you do. (Best seen
in the slideshare link)


## Which version of Python?

It's not a complete subset of any particular python, but it's based around the
intersection points in python 2 and 3.  It will be, by definition, a non-dynamic
subset - at least at first.

* For detail as to what's planned for the language, take a look at the language spec.
* For an overview as to the guiding principles, please take a look at project status
* For detail as to what's actually implemented, take a look at language status

These are all a WIP, but becoming more solid.


## Why write this?

Personally, having built something simpler in the past, I know I'd find it
useful. (I use python rather than C++ often because I can write more quicker
with the former). Also, I work with kids in my spare time, and it opens up
options there.

I've written something like this for work last year, but that was much more
limited and restricted in both aspiration and implementation. This rewrite is
something I've done on my own time, with my own tools, from scratch, which
allows me to share this with others.

Major changes:

* This aims to be a more rounded implementation
* This performs transforms from an AST (abstract syntax tree) to a CCR (concrete
  code representation), rather than munging code directly from a concrete parse
  tree.

That potentially allows other things, like creation of visual representations
of programs from code as well.


## Is this part of any larger project?

No. It could be used by others, but it's got a definite goal - to allow the
use of a "little" python to program devices which are too small to host a python
runtime.

If anything, it's a continuation of the personal itch around SWP (mentioned above)
from about 10 years ago. Unlike that though, it's much, much better structured.

One thing that may happen though is the ability to take python classes and
derive iotoy device implementations/interfaces directly. (since iotoy was
inspired heavily by python introspection) That's quite some time off.


## Release History

Release History:

* 0.0.17 - UNRELEASED - TBD
* 0.0.16 - 2015-08-02 - Adds initial Arduino LEONARDO support, improved function call, release build scripts
* 0.0.15 - 2015-07-18 - clib converted to py clib for adding to build directory
* 0.0.14 - 2015-07-18 - For loops implemented. Added clib code, C++ generator implementation, FOR loop style test harness, parsing and basic analysis of of FOR loops using a range interator
* 0.0.13 - 2015-06-21 - if/elif/else,conditionals/boolean/parenthesised expressions.
* 0.0.12 - 2015-06-16 - While loops, break/continue, Website, comparison operators, simple benchmark test
* 0.0.11 - 2015-06-06 - Function calls; inclusion of custom  C++ headers; empty statements; language spec updates
* 0.0.10 - 2015-06-03 - Analysis phase to make type inference work better. Lots of related changes. Implementation of expression statements.
* 0.0.9 - 2015-05-23 - Grammar changed to be left, not right recursive. (Fixes precedence in un-bracketed expressions) Added standalone compilation mode - outputs binaries from python code.
* 0.0.8 - 2015-05-13 - Internally switch over to using node objects for structure - resulting in better parsing of expressions with variables and better type inference.
* 0.0.7 - 2015-04-29 - Structural, testing improvements, infix operators expressions (+ - * / ) for integers, precdence fixes
* 0.0.6 - 2015-04-26 - Character Literals, "plus" expressions, build/test improvements
* 0.0.5 - 2015-04-23 - Core lexical analysis now matches language spec, including blocks
* 0.0.4 - 2015-04-22 - Mixed literals in print statements
* 0.0.3 - 2015-04-21 - Ability to print & work with a small number of variables
* 0.0.2 - 2015-03-30 - supports basic assignment
* 0.0.1 - Unreleased - rolled into 0.0.2 - Initial structure


## Language Status

    program : statements
    statements : statement
               | statement statements

    statement_block : INDENT statements DEDENT

    statement : assignment_statement
              | print_statement
              | general_expression
              | EOL
              | while_statement
              | break_statement
              | continue_statement
              | if_statement
              | for_statement

    assignment_statement -> IDENTIFIER ASSIGN general_expression # ASSIGN is currently limited to "="

    while_statement : WHILE general_expression COLON EOL statement_block

    break_statement : BREAK

    continue_statement : CONTINUE

    if_statement : IF general_expression COLON EOL statement_block
                 | IF general_expression COLON EOL statement_block extended_if_clauses

    extended_if_clauses : else_clause
                        | elif_clause

    else_clause : ELSE COLON EOL statement_block

    elif_clause : ELIF general_expression COLON EOL statement_block
                | ELIF general_expression COLON EOL statement_block extended_if_clauses

    print_statement : 'print' expr_list # Temporary - to be replaced by python 3 style function

    for_statement | FOR IDENTIFIER IN general_expression COLON EOL statement_block

    expr_list : general_expression
              | general_expression COMMA expr_list

    general_expression : boolean_expression

    boolean_expression : boolean_and_expression
                       | boolean_expression OR boolean_and_expression

    boolean_and_expression : boolean_not_expression
                           | boolean_and_expression AND boolean_not_expression

    boolean_not_expression : relational_expression
                           | NOT boolean_not_expression

    relational_expression : expression
                          | relational_expression COMPARISON_OPERATOR expression

    expression : arith_expression
               | expression '+' arith_expression
               | expression '-' arith_expression
               | expression '**' arith_expression

    arith_expression : expression_atom
                     | arith_expression '*' expression_atom
                     | arith_expression '/' expression_atom

    expression_atom : value_literal
                    | IDENTIFIER '(' ')' # Function call, with no arguments
                    | IDENTIFIER '(' expr_list ')' # Function call
                    | '(' general_expression ')'

    value_literal : number
                  | STRING
                  | CHARACTER
                  | BOOLEAN
                  | IDENTIFIER

    number : NUMBER
           | FLOAT
           | HEX
           | OCTAL
           | BINARY
           | '-' number

Current Lexing rules used by the grammar:

    NUMBER : \d+
    FLOAT : \d+.\d+ # different from normal python, which allows .1 and 1.
    HEX : 0x([abcdef]|\d)+
    OCTAL : 0o\d+
    BINARY : 0b\d+
    STRING - "([^\"]|\.)*" or '([^\']|\.)*' # single/double quote strings, with escaped values
    CHARACTER : c'.' /  c"." # Simplification - can be an escaped character
    BOOLEAN : True|False
    IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*


## Limitations

Most expressions currently rely on the C++ counterparts. As a result not all
combinations which are valid are directly supported yet. Notable ones:

* Combinations of strings with other strings (outlawing /*, etc)
* Combinations of strings with numbers 


## Why a python 2 print statement?

Python 2 has print statement with special notation; python 3's version is
a function call. The reason why this grammar currently has a python-2 style
print statement with special notation is to specifically avoid implementing
general function calls yet. Once those are implemented, special cases - like
implementing print - can be implemented, and this python 2 style print
statement WILL be removed. I expect this will occur around version 0.0.15,
based on current rate of progress.

Keeping it for now also simplifies "yield" later

Michael Sparks, August 2015


"""
#END
