# HLInt Demo Script (3 Members)

About 10 minutes. Each member runs their own part. Swap names in for **Member 1 / 2 / 3**.

| Part | Who | Topic | Time |
|---|---|---|---|
| 1 | Member 1 | Introduction, the HL language, how HLInt works | ~3 min |
| 2 | Member 2 | Live runs of PROG1–3 and the output files | ~3 min |
| 3 | Member 3 | Extra features, error detection, code walkthrough, closing | ~4 min |

---

## Before the demo (checklist)

- [ ] Pull the latest code: `git pull`
- [ ] Python 3.8+ installed: `python --version`
- [ ] Open a terminal **in the project folder** (where `HLInt.py` is).
- [ ] Increase the terminal font size so the audience can read it.
- [ ] Open `HLInt.py` in an editor (for Part 3).
- [ ] Do a dry run of every command below once, so nothing surprises you.
- [ ] Have `NOSPACES.TXT` and `RES_SYM.TXT` ready to open (they appear after the first run).

---

## Part 1 – Member 1: Introduction (~3 min)

**Say:**
> "Good day. We are [group name], and our project is **HLInt**, a simple interpreter for a hypothetical language called **HL**. It is written in Python."

> "HL is a small language. It has two data types, `integer` and `double`. You declare a variable with a colon, like `x: integer;`, and assign a value with `:=`, like `x := 5;`."

> "It supports addition and subtraction, printing with `output<<`, and a one-way `if` statement with the operators greater than, less than, equal, and not equal."

**Show** `tests/PROG3.HL` on screen while explaining:
```
x: integer;
y: double;
x:= 3;
if(x<5)
  output<<x;
```

**Say (how it works):**
> "When HLInt runs, it does five things:
> 1. It opens the HL source file.
> 2. It removes all spaces and saves the result to **NOSPACES.TXT**.
> 3. It saves every reserved word and symbol it finds to **RES_SYM.TXT**.
> 4. It checks for syntax errors and prints either **ERROR** or **NO ERROR(S) FOUND**.
> 5. If there are no errors, it runs the program and shows the output."

> "Member 2 will now show it running."

---

## Part 2 – Member 2: Live runs (~3 min)

### PROG1 – declaration, assignment, output
**Show the file**, then run:
```bash
python HLInt.py tests/PROG1.HL
```
**Expected:**
```
NO ERROR(S) FOUND
5
```
**Say:**
> "PROG1 declares `x` as an integer, assigns 5, and prints it. No errors were found, so it printed 5."

**Open `NOSPACES.TXT`:**
```
x:integer;
x:=5;
output<<x;
```
> "This is the program with all the spaces removed."

**Open `RES_SYM.TXT`** (one item per line):
```
:  integer  ;  :=  ;  output  <<  ;
```
> "These are the reserved words and symbols found, in the order they appear."

### PROG2 – adding an integer and a double
```bash
python HLInt.py tests/PROG2.HL
```
**Expected:**
```
NO ERROR(S) FOUND
4.25
```
**Say:**
> "`x` is the integer 3 and `y` is the double 1.25. Adding an integer and a double gives a double, printed with two decimal places: 4.25."

### PROG3 – one-way if
```bash
python HLInt.py tests/PROG3.HL
```
**Expected:**
```
NO ERROR(S) FOUND
3
```
**Say:**
> "`x` is 3, so the condition `x<5` is true and the output statement runs."

**Optional:** open `RES_SYM.TXT` again to show `if ( < )` now appears.

> "Member 3 will show more features and how errors are detected."

---

## Part 3 – Member 3: Extra features, errors, code (~4 min)

### EXTRA – strings, subtraction, `!=`, false condition
**Show `tests/EXTRA.HL`**, then run:
```bash
python HLInt.py tests/EXTRA.HL
```
**Expected:**
```
NO ERROR(S) FOUND
hello world
3.56
x is not 4
```
**Say:**
> "This program prints a string, computes `4 + 2.56` minus 3 which is 3.56, and uses `!=`. The last `if(x>5)` is false, so 'hidden' is **not** printed. That shows the one-way if skips its statement when the condition is false."

### ERR1 – missing semicolon
**Show `tests/ERR1.HL`** (line 2 has no `;`), then run:
```bash
python HLInt.py tests/ERR1.HL
```
**Expected:**
```
ERROR
  line 3: expected ; but found 'output'
```
**Say:**
> "Line 2 is missing a semicolon, so HLInt prints ERROR and does not run the program. It also tells us where the problem is."

### ERR2 – undeclared variable
```bash
python HLInt.py tests/ERR2.HL
```
**Expected:**
```
ERROR
  line 2: variable 'y' is not declared
```
**Say:**
> "Here `y` is used without being declared, so this is also an error."

### Optional live error (if time allows)
Edit `tests/PROG1.HL`, change `x:= 5;` to `x:= 5.5;`, save and run it:
```
NO ERROR(S) FOUND
RUNTIME ERROR
  line 2: cannot assign a double value to integer 'x'
```
> "Assigning a double to an integer is not allowed." **Undo the change afterwards.**

### Code walkthrough (open `HLInt.py`)
Scroll to each part and say one line about it:

| Function / class | What to say |
|---|---|
| `remove_spaces` | "Removes spaces for NOSPACES.TXT. Spaces inside strings are kept." |
| `tokenize` | "The lexer. It splits the source into tokens: reserved words, symbols, names, numbers and strings. Reserved words and symbols go to RES_SYM.TXT." |
| `Parser` | "A recursive-descent parser. It checks the grammar of each statement and raises an error with the line number if something is wrong." |
| `check_declarations` | "Checks that every variable is declared before use, before anything runs." |
| `Runtime` | "Executes the program: stores variables, does the math, keeps doubles to 2 decimals, and handles the if statement." |
| `main` | "Connects all the steps in order." |

### Closing
> "To summarize: HLInt reads an HL program, produces NOSPACES.TXT and RES_SYM.TXT, reports ERROR or NO ERROR(S) FOUND, and runs the program when it is valid. Thank you. We're open to questions."

---

## Possible questions (all members should know these)

| Question | Answer |
|---|---|
| Why Python? | Simple to read and quick to build a lexer and parser in. No extra libraries needed. |
| What is the difference between `:` and `:=`? | `:` declares a type (`x: integer;`). `:=` assigns a value (`x := 5;`). |
| Why does `x + y` give 4.25 and not 4? | Integer combined with double becomes a double. |
| Does it support multiplication or division? | No. The spec only asks for addition and subtraction. |
| Does it support `else`? | No. The spec asks for a one-way `if` only. |
| Why keep line breaks in NOSPACES.TXT? | To keep the file readable. Only spaces and tabs are removed. Can be changed to one line. |
| Is `Output` or `If` with a capital letter accepted? | Yes. Keywords are case-insensitive because the spec examples use both. |
| Does it accept `=` for assignment? | Yes. The spec uses both `=` and `:=`, so both work. |
| What happens if the file does not exist? | It prints `Cannot open file:` with the reason. |
| What is a token? | The smallest meaningful piece of code, like `x`, `:=`, `5` or `;`. |

---

## If something goes wrong during the demo

- **`python` not found:** try `py HLInt.py tests/PROG1.HL`.
- **File not found:** make sure the terminal is in the project folder (`ls` should show `HLInt.py`).
- **Unexpected output:** run `git status` / `git checkout tests/` to undo accidental edits to the test files.
