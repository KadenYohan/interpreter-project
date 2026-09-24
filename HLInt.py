"""HLInt.py - a simple interpreter for the hypothetical language "HL".

Usage:  python HLInt.py PROG1.HL

Steps performed:
  1. Read the HL source file.
  2. Write the program without spaces to NOSPACES.TXT.
  3. Write the reserved words and symbols found to RES_SYM.TXT.
  4. Check syntax: print "ERROR" or "NO ERROR(S) FOUND".
  5. If there are no errors, execute the program.
"""
import sys

RESERVED = {"integer", "double", "output", "if"}
SYMBOLS = [":=", "<<", "==", "!=", ":", ";", "=", "+", "-", "(", ")", "<", ">"]
RELOPS = {"<", ">", "==", "!="}


class HLError(Exception):
    def __init__(self, msg, line):
        super().__init__(msg)
        self.line = line


# ---------------------------------------------------------------- step 2
def remove_spaces(src):
    """Remove spaces/tabs (kept inside string literals); newlines are kept."""
    out, in_str = [], False
    for ch in src:
        if ch == '"':
            in_str = not in_str
        if ch in " \t\r" and not in_str:
            continue
        out.append(ch)
    return "".join(out)


# ---------------------------------------------------------------- lexer
def tokenize(src):
    """Return list of (kind, value, line). kinds: RES, SYM, ID, INT, DBL, STR."""
    tokens, i, line, n = [], 0, 1, len(src)
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
        elif c in " \t\r":
            i += 1
        elif c == '"':
            j = src.find('"', i + 1)
            if j == -1 or "\n" in src[i:j]:
                raise HLError("unterminated string", line)
            tokens.append(("STR", src[i + 1:j], line))
            i = j + 1
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            word = src[i:j]
            if word.lower() in RESERVED:
                tokens.append(("RES", word.lower(), line))
            else:
                tokens.append(("ID", word, line))
            i = j
        elif c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            if j < n and src[j] == ".":
                j += 1
                if j >= n or not src[j].isdigit():
                    raise HLError("malformed number", line)
                while j < n and src[j].isdigit():
                    j += 1
                tokens.append(("DBL", src[i:j], line))
            else:
                tokens.append(("INT", src[i:j], line))
            i = j
        else:
            for s in SYMBOLS:
                if src.startswith(s, i):
                    tokens.append(("SYM", s, line))
                    i += len(s)
                    break
            else:
                raise HLError("unknown character '%s'" % c, line)
    return tokens


# ---------------------------------------------------------------- parser
class Parser:
    """Recursive-descent parser; builds a list of statement tuples."""

    def __init__(self, tokens):
        self.t, self.p = tokens, 0

    def peek(self):
        return self.t[self.p] if self.p < len(self.t) else ("EOF", "", self.t[-1][2] if self.t else 1)

    def next(self):
        tok = self.peek()
        self.p += 1
        return tok

    def expect(self, kind, value=None, what=None):
        tok = self.next()
        if tok[0] != kind or (value is not None and tok[1] != value):
            want = what or value or kind
            got = "end of file" if tok[0] == "EOF" else "'%s'" % tok[1]
            raise HLError("expected %s but found %s" % (want, got), tok[2])
        return tok

    def program(self):
        stmts = []
        while self.peek()[0] != "EOF":
            stmts.append(self.statement())
        return stmts

    def statement(self):
        kind, val, line = self.peek()
        if kind == "ID":
            self.next()
            op = self.next()
            if op[1] == ":" and op[0] == "SYM":
                ty = self.next()
                if ty[0] != "RES" or ty[1] not in ("integer", "double"):
                    raise HLError("expected data type 'integer' or 'double'", ty[2])
                self.expect("SYM", ";")
                return ("decl", val, ty[1], line)
            if op[0] == "SYM" and op[1] in (":=", "="):
                e = self.expr()
                self.expect("SYM", ";")
                return ("assign", val, e, line)
            raise HLError("expected ':' or ':=' after '%s'" % val, op[2])
        if kind == "RES" and val == "output":
            self.next()
            self.expect("SYM", "<<")
            if self.peek()[0] == "STR":
                e = ("str", self.next()[1])
            else:
                e = self.expr()
            self.expect("SYM", ";")
            return ("output", e, line)
        if kind == "RES" and val == "if":
            self.next()
            self.expect("SYM", "(")
            left = self.expr()
            op = self.next()
            if op[0] != "SYM" or op[1] not in RELOPS:
                raise HLError("expected one of > < == !=", op[2])
            right = self.expr()
            self.expect("SYM", ")")
            body = self.statement()
            return ("if", left, op[1], right, body, line)
        raise HLError("unexpected '%s'" % (val or "end of file"), line)

    def expr(self):
        node = self.term()
        while self.peek()[0] == "SYM" and self.peek()[1] in ("+", "-"):
            op = self.next()[1]
            node = ("bin", op, node, self.term())
        return node

    def term(self):
        kind, val, line = self.next()
        if kind == "INT":
            return ("num", int(val), "integer", line)
        if kind == "DBL":
            return ("num", round(float(val), 2), "double", line)
        if kind == "ID":
            return ("var", val, line)
        raise HLError("expected a number or variable but found '%s'" % (val or "end of file"), line)


# ---------------------------------------------------------------- semantics / run
class Runtime:
    def __init__(self):
        self.types, self.vals, self.out = {}, {}, []

    def evaluate(self, e):
        """Return (value, type)."""
        if e[0] == "num":
            return e[1], e[2]
        if e[0] == "var":
            name, line = e[1], e[2]
            if name not in self.types:
                raise HLError("variable '%s' is not declared" % name, line)
            if name not in self.vals:
                raise HLError("variable '%s' has no value yet" % name, line)
            return self.vals[name], self.types[name]
        _, op, l, r = e
        (a, ta), (b, tb) = self.evaluate(l), self.evaluate(r)
        v = a + b if op == "+" else a - b
        if ta == tb == "integer":
            return v, "integer"
        return round(v, 2), "double"

    def fmt(self, v, t):
        return str(v) if t == "integer" else "%.2f" % v

    def run(self, stmts):
        for s in stmts:
            self.exec(s)

    def exec(self, s):
        k = s[0]
        if k == "decl":
            _, name, ty, line = s
            if name in self.types:
                raise HLError("variable '%s' already declared" % name, line)
            self.types[name] = ty
        elif k == "assign":
            _, name, e, line = s
            if name not in self.types:
                raise HLError("variable '%s' is not declared" % name, line)
            v, t = self.evaluate(e)
            if self.types[name] == "integer" and t == "double":
                raise HLError("cannot assign a double value to integer '%s'" % name, line)
            self.vals[name] = float(v) if self.types[name] == "double" else v
        elif k == "output":
            e = s[1]
            if e[0] == "str":
                print(e[1])
            else:
                print(self.fmt(*self.evaluate(e)))
        elif k == "if":
            _, l, op, r, body, line = s
            a, b = self.evaluate(l)[0], self.evaluate(r)[0]
            if {"<": a < b, ">": a > b, "==": a == b, "!=": a != b}[op]:
                self.exec(body)


def check_declarations(stmts):
    """Static semantic check so 'ERROR' is reported before anything runs."""
    declared = {}

    def check_expr(e):
        if e[0] == "var" and e[1] not in declared:
            raise HLError("variable '%s' is not declared" % e[1], e[2])
        if e[0] == "bin":
            check_expr(e[2]); check_expr(e[3])

    def check(s):
        if s[0] == "decl":
            if s[1] in declared:
                raise HLError("variable '%s' already declared" % s[1], s[3])
            declared[s[1]] = s[2]
        elif s[0] == "assign":
            if s[1] not in declared:
                raise HLError("variable '%s' is not declared" % s[1], s[3])
            check_expr(s[2])
        elif s[0] == "output":
            if s[1][0] != "str":
                check_expr(s[1])
        elif s[0] == "if":
            check_expr(s[1]); check_expr(s[3]); check(s[4])

    for s in stmts:
        check(s)


# ---------------------------------------------------------------- main
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else input("HL source file: ").strip()
    try:
        with open(path, encoding="utf-8") as f:
            src = f.read()
    except OSError as e:
        print("Cannot open file:", e)
        return 1

    with open("NOSPACES.TXT", "w", encoding="utf-8") as f:
        f.write(remove_spaces(src))

    try:
        tokens = tokenize(src)
    except HLError as e:
        open("RES_SYM.TXT", "w").close()
        print("ERROR\n  line %d: %s" % (e.line, e))
        return 1

    with open("RES_SYM.TXT", "w", encoding="utf-8") as f:
        for kind, val, _ in tokens:
            if kind in ("RES", "SYM"):
                f.write(val + "\n")

    try:
        stmts = Parser(tokens).program()
        check_declarations(stmts)
    except HLError as e:
        print("ERROR\n  line %d: %s" % (e.line, e))
        return 1
    print("NO ERROR(S) FOUND")

    try:
        Runtime().run(stmts)
    except HLError as e:
        print("RUNTIME ERROR\n  line %d: %s" % (e.line, e))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
