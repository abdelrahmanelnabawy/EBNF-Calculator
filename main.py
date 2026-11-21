
class Expression:
    def __init__(self, tk):
        self.tokens = self.__tokenize(tk)
        self.pos = 0

    def __tokenize(self, tk):
        tokens = []
        temp = ''
        for char in tk:
            if char in '()+-*/^' or char.isspace():
                if temp:
                    tokens.append(temp)
                    temp = ''
                if not char.isspace():
                    tokens.append(char)
            elif char.isdigit():
                temp += char
            else:
                raise ValueError(f"Invalid character: {char}")
        if temp:
            tokens.append(temp)
        return tokens

    def __peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def __consume(self):
        token = self.__peek()
        self.pos += 1
        return token

    def __expr(self):
        result = self.__term()
        while self.__peek() in ('+', '-'):
            op = self.__consume()
            right = self.__term()
            if op == '+':
                result += right
            else:
                result -= right
        return result

    def __expo(self):
        result = self.__factor()
        if self.__peek() == '^':
            self.__consume()
            right = self.__expo()
            result = result ** right
        return result

    def __term(self):
        result = self.__expo()
        while self.__peek() in ('*', '/'):
            op = self.__consume()
            right = self.__expo()
            if op == '*':
                result *= right
            else:
                result /= right
        return result

    def __factor(self):
        token = self.__consume()
        if token is None:
            raise ValueError("Unexpected end of expression")
        if token == '(':
            result = self.__expr()
            if self.__consume() != ')':
                raise ValueError("Expected ')'")
            return result
        elif token.isdigit():
            return int(token)
        else:
            raise ValueError(f"Unexpected token: {token}")

    def evaluate(self):
        self.pos = 0
        result = self.__expr()
        if self.pos < len(self.tokens):
            raise ValueError(f"Unexpected token at end: {self.tokens[self.pos]}")
        return result


def test():
    expr = Expression("2+3*4")
    assert expr.tokens == ['2', '+', '3', '*', '4']
    assert expr.evaluate() == 14

    expr = Expression("2^5*7+6")
    assert expr.tokens == ['2', '^', '5', '*', '7', '+', '6']
    assert expr.evaluate() == 230

    expr = Expression("2^4+3^2")
    assert expr.tokens == ['2', '^', '4', '+', '3', '^', '2']
    assert expr.evaluate() == 25

    print("All tests passed.")

if __name__ == "__main__":
    expr = Expression("2^2^2^2+5*3")
    print(expr.tokens)  # Output: ['2', '^', '5', '*', '7', '+', '
    print(expr.evaluate())  # Output: 230
    # test()