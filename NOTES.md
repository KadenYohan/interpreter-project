# HLInt – Project Notes (CSS125L)

Context for group members on what was built and why. Read this before touching the code or writing the documentation.

## What the project is
The specs (`CSS125P Project Specifications.docx`) ask for a simple interpreter, **HLInt.XXX**, for a hypothetical language called **HL**. We named ours `HLInt.py` (Python 3.11). The documentation must follow `CSS125P Project_Template.docx` and be submitted as **one PDF, by one member only**.

## The HL language (as implemented)
| Feature | Syntax | Notes |
|---|---|---|
| Declaration | `x: integer;` `y: double;` | Two types only. Redeclaring is an error. |
| Assignment | `x := 5;` `y := 2.35;` | `=` is also accepted because the spec mixes `:=` and `=`. |
| Math | `3 + 2`, `4 + 2.56`, `x - y` | Only `+` and `-`. Int + double gives double. Doubles keep 2 decimals. |
| Output | `output<<"text";` `output<<x;` `output<<x+y;` | Doubles print as `4.25`, integers as `5`. |
| One-way if | `if(x<5) output<<x;` | Operators: `>` `<` `==` `!=`. Body is a single statement. |

Keywords (`integer`, `double`, `output`, `if`) are case-insensitive since the spec shows `If` and `Output`.

## What the interpreter does (the "Process" in the specs)
Run: `python HLInt.py tests/PROG1.HL`

1. Opens the `.HL` file.
2. Writes the program without spaces to **`NOSPACES.TXT`**.
3. Writes every reserved word and symbol found (one per line, in order) to **`RES_SYM.TXT`**.
4. Prints **`ERROR`** (plus a line number and reason) or **`NO ERROR(S) FOUND`**.
5. Only if there are no errors, runs the program.

Both `.TXT` files are overwritten on every run, in the folder you run from.

## How the code is organised (`HLInt.py`)
- `remove_spaces` – step 2.
- `tokenize` – lexer. Produces tokens: reserved word, symbol, identifier, integer, double, string. Feeds `RES_SYM.TXT`.
- `Parser` – recursive-descent parser. Statements: declaration, assignment, output, if. Expressions are `term (+|- term)*`. Syntax errors are raised here.
- `check_declarations` – static check for undeclared or redeclared variables, done before running so `ERROR` is reported before any output.
- `Runtime` – evaluates and executes. Handles types, 2-decimal rounding, and the runtime errors (use before assignment, double assigned to integer).
- `main` – ties the steps together.

## Test programs (`tests/`)
| File | Expected result |
|---|---|
| `PROG1.HL` | `NO ERROR(S) FOUND`, then `5` |
| `PROG2.HL` | `NO ERROR(S) FOUND`, then `4.25` |
| `PROG3.HL` | `NO ERROR(S) FOUND`, then `3` |
| `EXTRA.HL` | strings, subtraction, `!=`; prints `hello world`, `3.56`, `x is not 4` |
| `ERR1.HL` | `ERROR` – missing `;` on line 3 |
| `ERR2.HL` | `ERROR` – `y` used but not declared |

All were run and matched. PROG1–3 are copied from the specs.

## Decisions we made (change if the instructor says otherwise)
- **NOSPACES.TXT** removes spaces and tabs but keeps line breaks and spaces inside `"strings"`. Making it one continuous line is a one-line change in `remove_spaces`.
- **ERROR output** has an extra detail line after the word `ERROR`. Remove it if the specs mean the word only.
- **Single-digit integers** are not enforced (`12` works).
- Program output is shown only when there are no errors.

## Still to do
- [ ] Fill in the documentation using the template: group name, members with sections, Introduction, Constructs Supported (data types, declarations, expressions, I/O), Screenshots, Source Code, References.
- [ ] Take screenshots of real runs (PROG1–3 and at least one ERROR case; show `NOSPACES.TXT` and `RES_SYM.TXT` too).
- [ ] Paste the final `HLInt.py` into the Source Code section.
- [ ] Export as PDF; only one member submits.
- [ ] Optional: confirm the ambiguities above with the instructor.
