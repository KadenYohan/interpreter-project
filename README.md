# HLInt – A Simple Interpreter for the "HL" Language

## I. Introduction

### a. Description of the Program

**HLInt** (`HLInt.py`) is a simple interpreter, written in Python 3, for a small hypothetical language called **HL**. It reads an HL source file (for example `PROG1.HL`), checks it for errors, and then runs it.

When HLInt runs, it does the following:

1. Opens the HL source file.
2. Removes all spaces from the program and writes the result to `NOSPACES.TXT`.
3. Writes the reserved words and symbols found in the program to `RES_SYM.TXT`, one per line.
4. Prints `ERROR` (with the line number and reason) if it finds a syntax error, or `NO ERROR(S) FOUND` if the program is correct.
5. If there are no errors, executes the program and prints its output on the screen.

**How to run**

```bash
python HLInt.py tests/PROG1.HL
```

Requires Python 3.8 or newer. No other libraries are needed.

**Project files**

| File | Purpose |
|---|---|
| `HLInt.py` | The interpreter |
| `tests/` | Sample HL programs (`PROG1–3.HL` from the specs, `EXTRA.HL`, and error cases `ERR1.HL`, `ERR2.HL`) |
| `NOTES.md` | Development notes and decisions |
| `NOSPACES.TXT`, `RES_SYM.TXT` | Generated on every run |

## II. Constructs Supported

### a. Data types

| Type | Description | Example values |
|---|---|---|
| `integer` | Whole numbers | `5`, `3` |
| `double` | Decimal numbers, kept to a precision of 2 decimal places | `2.35`, `1.25` |

Assigning a `double` value to an `integer` variable is an error. Assigning an integer to a `double` variable is allowed.

### b. Variable declarations

A variable must be declared before it is used. The form is `name: type;`

```
x: integer;
y: double;
```

Declaring the same variable twice, or using an undeclared variable, is reported as an error. Assignment uses `:=` (`=` is also accepted):

```
x := 5;
y := 2.35;
```

### c. Expressions and operations

**Arithmetic:** addition (`+`) and subtraction (`-`) on integers and doubles.

```
x := 3 + 2;
y := 4 + 2.56;
```

An integer combined with a double gives a double, shown with 2 decimal places (for example `3 + 1.25` gives `4.25`).

**Conditional statement:** a one-way `if` with a single statement as its body. Supported comparison operators are `>`, `<`, `==` and `!=`.

```
if(x<5)
   output<<x;
```

If the condition is false, the statement is skipped.

### d. Input/Output statements

HL supports output only, using `output<<`. It can print a string, a variable, or an expression.

```
output<<"hello";
output<<x;
output<<x+y;
```

Integers are printed as they are (`5`). Doubles are printed with 2 decimal places (`4.25`).

**Sample program (`PROG2.HL`)**

```
x: integer;
y: double;
x:= 3;
y:= 1.25;
output<<x+y;
```

Output:

```
NO ERROR(S) FOUND
4.25
```
