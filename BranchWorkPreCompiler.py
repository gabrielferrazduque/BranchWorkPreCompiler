
import re, sys

Scanner Léxico
TOKEN_REGEX = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('MAIN', r'\bmain\b'),
    ('TYPE', r'\b(int|float|char)\b'),
    ('IF', r'\bif\b'), ('ELSE', r'\belse\b'), ('WHILE', r'\bwhile\b'),
    ('DO', r'\bdo\b'), ('FOR', r'\bfor\b'),
    ('FLOAT_CONST', r'\d+\.\d+'), ('INT_CONST', r'\d+'),
    ('CHAR_CONST', r"'.'"),
    ('ID', r'[_a-zA-Z][_a-zA-Z0-9]*'),
    ('OP_REL', r'<=|>=|==|!=|<|>'),
    ('OP_ARITH', r'[+\-*/=]'),
    ('SYMBOL', r'[(){},;]'),
    ('NEWLINE', r'\n'), ('SKIP', r'[ \t]+'),
    ('INVALID', r'.')
]

TOKEN_RE = re.compile('|'.join(f'(?P<{n}>{r})' for n, r in TOKEN_REGEX))

class Scanner:
    def __init__(self, code): self.code, self.line, self.col = code, 1, 1
    def tokenize(self):
        tokens, pos = [], 0
        while pos < len(self.code):
            match = TOKEN_RE.match(self.code, pos)
            kind, value = match.lastgroup, match.group()
            if kind == 'NEWLINE': self.line, self.col = self.line+1, 1
            elif kind == 'SKIP' or kind == 'COMMENT': pass
            elif kind == 'INVALID':
                raise Exception(f"Erro léxico: '{value}' linha {self.line}")
            else: tokens.append((kind, value, self.line, self.col))
            pos, self.col = match.end(), self.col + len(value)
        tokens.append(('EOF', '', self.line, self.col))
        return tokens

# Parser, Tabela de Símbolos e Analisador Semântico
class SymbolTable:
    def __init__(self): self.scopes = [{}]
    def push_scope(self): self.scopes.append({})
    def pop_scope(self): self.scopes.pop()
    def declare(self, id, type):
        if id in self.scopes[-1]: raise Exception(f"Redeclarado: {id}")
        self.scopes[-1][id] = type
    def lookup(self, id):
        for scope in reversed(self.scopes):
            if id in scope: return scope[id]
        raise Exception(f"Não declarado: {id}")
              def match(self, kind, value=None):
    current = self.current()
    if current.type == kind and (value is None or current.value == value):
        self.advance()
    else:
        raise RuntimeError(f"Expected {kind}{' with value ' + value if value else ''}, but got {current}")
class Parser:
    def __init__(self, tokens): self.tokens, self.pos, self.symtab, self.code, self.temp = tokens, 0, SymbolTable(), [], 0
    def current(self): return self.tokens[self.pos]
    def match(self, type, val=None):
        tok = self.current()
        if tok[0] == type and (val is None or tok[1] == val): self.pos += 1
        else: raise Exception(f"Esperado {type} mas encontrou {tok}")
    def program(self):
        self.match('TYPE', 'int'); self.match('MAIN'); self.match('SYMBOL', '(')
        self.match('SYMBOL', ')'); self.block()
    def block(self):
        self.symtab.push_scope(); self.match('SYMBOL', '{')
        while self.current()[0] == 'TYPE': self.decl()
        while self.current()[1] != '}': self.stmt()
        self.match('SYMBOL', '}'); self.symtab.pop_scope()
    def decl(self):
        type = self.current()[1]; self.match('TYPE')
        while True:
            id = self.current()[1]; self.symtab.declare(id, type); self.match('ID')
            if self.current()[1] == ';': break
            self.match('SYMBOL', ',')
        self.match('SYMBOL', ';')
    def stmt(self):
        id = self.current()[1]; self.match('ID'); self.match('OP_ARITH', '=')
        typ, val = self.expr(); sym_typ = self.symtab.lookup(id)
        if sym_typ != typ: raise Exception("Erro semântico: tipos incompatíveis")
        self.match('SYMBOL', ';'); self.code.append(f'{id} = {val}')
    def expr(self):
        tok = self.current()
        if tok[0] in ('INT_CONST', 'FLOAT_CONST', 'CHAR_CONST'):
            self.match(tok[0]); return ('int' if tok[0]=='INT_CONST' else 'float', tok[1])
        elif tok[0] == 'ID':
            self.match('ID'); return (self.symtab.lookup(tok[1]), tok[1])
        else: raise Exception("Erro sintático: expressão inválida")

# Geração de Código Intermediário
def compile_source(source):
    scanner = Scanner(source); tokens = scanner.tokenize()
    parser = Parser(tokens); parser.program()
    return parser.code
  
if __name__ == '__main__': 
    if len(sys.argv) != 2: print("Uso: python compiler.py <arquivo>"); exit(1)
    with open(sys.argv[1]) as f: code = f.read()
    intermediate_code = compile_source(code)
    print("Código Intermediário:")
    for line in intermediate_code: print(line) 
self.match('(') self.match('SYMBOL', '('). 
    
int main() {
    int x, y;
    x = 3;
    y = x + 5;
} 
  1
 int();x = 3
2
double();t1 = x + 5
3
main();y = t1
} 
return
