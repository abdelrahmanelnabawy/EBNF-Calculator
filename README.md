# Grammar Calculator

A recursive-descent expression evaluator written in Python. It parses and calculates arithmetic expressions based on formal EBNF grammar rules, respecting operator precedence and associativity.

---

## Grammar Specification (EBNF)

The parser implements the following context-free grammar:

```ebnf
expr   := term { ('+' | '-') term } ;
term   := expo { ('*' | '/') expo } ;
expo   := factor [ '^' expo ] ;
factor := number | '(' expr ')' ;
```

### Precedence & Associativity

| Level | Rule | Operators | Associativity | Description |
|:---:|:---:|:---:|:---:|:---|
| **1 (Lowest)** | `expr` | `+`, `-` | Left-to-right | Addition, Subtraction |
| **2** | `term` | `*`, `/` | Left-to-right | Multiplication, Division |
| **3** | `expo` | `^` | Right-to-left | Exponentiation (e.g. `2^3^2 = 2^(3^2) = 512`) |
| **4 (Highest)**| `factor` | `(...)`, `number` | N/A | Grouped expressions, integers |

---

## Features

- **Lexer / Tokenizer**: Handles multi-digit numbers, operators (`+`, `-`, `*`, `/`, `^`), parentheses, and arbitrary whitespace.
- **Recursive Descent Parser**: Direct translation of grammar rules into predictive parsing methods.
- **Operator Precedence**: Correct evaluation order without relying on `eval()`.
- **Right-Associative Exponentiation**: `2^3^2` evaluates as $2^{(3^2)} = 512$.
- **Error Handling**: Detects and reports invalid characters, mismatched parentheses, unexpected tokens, and malformed expressions.

---

## File Structure

```text
grammer_calculater/
├── main.py        # Expression class with tokenizer and parser
├── test.py        # Comprehensive test suite using unittest
└── README.md      # Documentation and grammar details
```

---

## Usage

You can import and use the `Expression` class in your Python scripts:

```python
from main import Expression

# 1. Simple expression with precedence
expr = Expression("2 + 3 * 4")
print(expr.tokens)     # ['2', '+', '3', '*', '4']
print(expr.evaluate()) # 14

# 2. Exponentiation with right-associativity
expr = Expression("2 ^ 3 ^ 2")
print(expr.evaluate()) # 512

# 3. Parentheses and multi-digit integers
expr = Expression("((10 + 5) * 2) / 3")
print(expr.evaluate()) # 10.0
```

---

## Running the Tests

To run the test suite:

```bash
python3 test.py
```

or via `unittest`:

```bash
python3 -m unittest test.py -v
```
