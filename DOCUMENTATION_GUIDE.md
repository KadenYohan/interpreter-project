# Documentation Guide (CSS125P Project Template)

What to put in each part of `CSS125P Project_Template.docx`. Copy the text into the Word template, keep the template's headings and formatting, then **export as PDF**. Only **one member** submits.

Group Name and Group Members are left for you to fill in.

---

## Groupings

- **Group Name:** _(fill in)_
- **Group Members (including section of each student):** _(fill in all 3 names + sections)_

---

## Introduction

### Description of the Program

> HLInt is a simple interpreter, written in Python 3, for a hypothetical programming language called HL. It reads an HL source file (such as PROG1.HL, PROG2.HL or PROG3.HL), checks it for errors, and executes it.
>
> When HLInt runs, it performs the following steps:
> 1. It opens the HL source file given by the user.
> 2. It removes all spaces from the program and writes the result to an output file named NOSPACES.TXT.
> 3. It identifies the reserved words and symbols in the program and writes them to RES_SYM.TXT.
> 4. It checks the program for syntax errors and prints "ERROR" if any are found, or "NO ERROR(S) FOUND" if there are none.
> 5. If no errors are found, it executes the program and displays its output on the screen.
>
> The interpreter is made of four main parts: a lexer that breaks the source code into tokens, a recursive-descent parser that checks the grammar, a semantic checker that verifies all variables are declared before use, and a runtime that executes the statements.
>
> To run the program: `python HLInt.py PROG1.HL`

---

## Constructs Supported

### Data types

> HL supports two data types:
>
> | Data type | Description | Example |
> |---|---|---|
> | integer | Whole numbers | 5, 3 |
> | double | Decimal numbers with a precision of 2 decimal places | 2.35, 1.25 |
>
> An integer value may be assigned to a double variable, but assigning a double value to an integer variable produces an error.

### Variable declarations

> Every variable must be declared before it is used. A declaration has the form `variable: datatype;`
>
> ```
> x: integer;
> y: double;
> ```
>
> Values are assigned using the `:=` operator:
>
> ```
> x := 5;
> y := 2.35;
> ```
>
> Using a variable that has not been declared, or declaring the same variable twice, is reported as an error.

### Expressions and operations

> **Arithmetic operations:** HL supports addition (`+`) and subtraction (`-`) of integer and double values.
>
> ```
> x := 3 + 2;
> y := 4 + 2.56;
> ```
>
> When an integer and a double are combined, the result is a double, rounded to 2 decimal places. For example, `3 + 1.25` gives `4.25`.
>
> **Conditional statement:** HL supports a one-way `if` statement. If the condition is true, the statement that follows is executed; otherwise it is skipped. The relational operators supported are `>`, `<`, `==` and `!=`.
>
> ```
> x := 6;
> if(x<5)
>    output<<x;
> ```

### Input/Output statements

> HL supports output statements using `output<<`. A string, a variable, or an expression can be printed.
>
> ```
> output<<"hello";
> output<<x;
> output<<x+y;
> ```
>
> Integer values are displayed as they are (e.g. `5`), and double values are displayed with 2 decimal places (e.g. `4.25`). HL does not have an input statement; the program's data comes from the assignments in the source file.

---

## Code and References

### Screenshots of Sample Runs

Take these screenshots from the real program (see `DEMO_SCRIPT.md` for the commands and expected output). Put a short caption under each one.

| # | Screenshot | Caption to use |
|---|---|---|
| 1 | `python HLInt.py tests/PROG1.HL` | Figure 1. Sample run of PROG1.HL |
| 2 | `NOSPACES.TXT` after PROG1 | Figure 2. NOSPACES.TXT generated from PROG1.HL |
| 3 | `RES_SYM.TXT` after PROG1 | Figure 3. RES_SYM.TXT generated from PROG1.HL |
| 4 | `python HLInt.py tests/PROG2.HL` | Figure 4. Sample run of PROG2.HL |
| 5 | `python HLInt.py tests/PROG3.HL` | Figure 5. Sample run of PROG3.HL |
| 6 | `python HLInt.py tests/EXTRA.HL` | Figure 6. Strings, subtraction and != |
| 7 | `python HLInt.py tests/ERR1.HL` | Figure 7. Syntax error: missing semicolon |
| 8 | `python HLInt.py tests/ERR2.HL` | Figure 8. Error: undeclared variable |

Tips: show the HL source next to the output if possible, use a readable font size, and crop out unrelated windows.

### Source Code

Paste the **full contents of `HLInt.py`** from the repository. Use a monospace font (e.g. Consolas, 9–10 pt) and keep the indentation. Optionally include the test programs (`tests/*.HL`) after it.

### References

> - CSS125L Project Specifications: A Simple "Interpreter". Mapúa University.
> - Python Software Foundation. (n.d.). *Python 3 documentation*. https://docs.python.org/3/
> - Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.
> - Nystrom, R. (2021). *Crafting Interpreters*. https://craftinginterpreters.com/
> - Anthropic. (2026). *Claude* [AI assistant]. Used to help write and test the interpreter.

Keep only references you actually used, and add your course lecture notes if you referred to them. Check whether your instructor allows AI tools and how they want them cited.

---

## Final checklist before submitting

- [ ] Group name and all 3 members with sections filled in
- [ ] Every template heading is present, in the same order
- [ ] Screenshots are from real runs of the final code
- [ ] Full `HLInt.py` is included
- [ ] References filled in
- [ ] Saved/exported as **PDF**
- [ ] Only **one** member uploads it
