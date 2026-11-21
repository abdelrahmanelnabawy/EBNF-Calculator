import unittest
from main import Expression

# an AI generated Test.


class TestExpressionTokenizer(unittest.TestCase):
    def test_single_digits_and_operators(self):
        expr = Expression("1+2*3/4-5^6")
        self.assertEqual(
            expr.tokens,
            ['1', '+', '2', '*', '3', '/', '4', '-', '5', '^', '6']
        )

    def test_multi_digit_numbers(self):
        expr = Expression("120 + 3456 * 78")
        self.assertEqual(expr.tokens, ['120', '+', '3456', '*', '78'])

    def test_whitespace_handling(self):
        expr = Expression("   42   \t + \n 18   ")
        self.assertEqual(expr.tokens, ['42', '+', '18'])

    def test_parentheses_tokenization(self):
        expr = Expression("(10 + (20 * 3))")
        self.assertEqual(expr.tokens, ['(', '10', '+', '(', '20', '*', '3', ')', ')'])

    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            Expression("2 + 3 & 4")

        with self.assertRaises(ValueError):
            Expression("foo + bar")


class TestExpressionEvaluation(unittest.TestCase):
    def test_single_number(self):
        self.assertEqual(Expression("0").evaluate(), 0)
        self.assertEqual(Expression("42").evaluate(), 42)
        self.assertEqual(Expression("100500").evaluate(), 100500)

    def test_basic_addition_and_subtraction(self):
        self.assertEqual(Expression("2 + 3").evaluate(), 5)
        self.assertEqual(Expression("10 - 4").evaluate(), 6)
        # Left-associative subtraction: (10 - 4) - 2 = 4
        self.assertEqual(Expression("10 - 4 - 2").evaluate(), 4)
        self.assertEqual(Expression("5 + 3 - 2 + 1").evaluate(), 7)

    def test_basic_multiplication_and_division(self):
        self.assertEqual(Expression("3 * 4").evaluate(), 12)
        self.assertEqual(Expression("20 / 4").evaluate(), 5.0)
        # Left-associative division: (100 / 10) / 2 = 5.0
        self.assertEqual(Expression("100 / 10 / 2").evaluate(), 5.0)
        self.assertEqual(Expression("2 * 3 * 4").evaluate(), 24)

    def test_precedence_multiplication_over_addition(self):
        self.assertEqual(Expression("2 + 3 * 4").evaluate(), 14)
        self.assertEqual(Expression("2 * 3 + 4").evaluate(), 10)
        self.assertEqual(Expression("20 - 2 * 3 + 4 / 2").evaluate(), 16.0)

    def test_exponentiation(self):
        self.assertEqual(Expression("2 ^ 3").evaluate(), 8)
        self.assertEqual(Expression("5 ^ 0").evaluate(), 1)
        # Precedence: ^ has higher precedence than * and +
        self.assertEqual(Expression("2 ^ 5 * 7 + 6").evaluate(), 230)
        self.assertEqual(Expression("2 ^ 4 + 3 ^ 2").evaluate(), 25)

    def test_exponentiation_right_associativity(self):
        # Right-associative: 2 ^ (3 ^ 2) = 2 ^ 9 = 512, NOT (2 ^ 3) ^ 2 = 64
        self.assertEqual(Expression("2 ^ 3 ^ 2").evaluate(), 512)
        # 2 ^ (2 ^ (2 ^ 2)) = 2 ^ (2 ^ 4) = 2 ^ 16 = 65536
        self.assertEqual(Expression("2 ^ 2 ^ 2 ^ 2").evaluate(), 65536)

    def test_parentheses(self):
        self.assertEqual(Expression("(2 + 3) * 4").evaluate(), 20)
        self.assertEqual(Expression("2 * (3 + 4)").evaluate(), 14)
        self.assertEqual(Expression("((2 + 3) * (4 - 2)) ^ 2").evaluate(), 100)
        self.assertEqual(Expression("(2 ^ 3) ^ 2").evaluate(), 64)

    def test_complex_expressions(self):
        expr = Expression("2 ^ 2 ^ 2 ^ 2 + 5 * 3")
        self.assertEqual(expr.evaluate(), 65551)

        expr = Expression("10 + 2 * (3 + 4 ^ 2) - 8 / 2")
        # 10 + 2 * (3 + 16) - 4 = 10 + 2 * 19 - 4 = 10 + 38 - 4 = 44.0
        self.assertEqual(expr.evaluate(), 44.0)


class TestExpressionErrors(unittest.TestCase):
    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            Expression("").evaluate()

        with self.assertRaises(ValueError):
            Expression("    ").evaluate()

    def test_unmatched_parentheses(self):
        with self.assertRaises(ValueError):
            Expression("(2 + 3").evaluate()

        with self.assertRaises(ValueError):
            Expression("2 + 3)").evaluate()

        with self.assertRaises(ValueError):
            Expression("((2 + 3) * 4").evaluate()

    def test_trailing_unexpected_tokens(self):
        with self.assertRaises(ValueError):
            Expression("2 + 3 4").evaluate()

    def test_missing_operand(self):
        with self.assertRaises(ValueError):
            Expression("2 + ").evaluate()

        with self.assertRaises(ValueError):
            Expression("* 4").evaluate()

        with self.assertRaises(ValueError):
            Expression("2 + * 3").evaluate()

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            Expression("10 / 0").evaluate()


if __name__ == "__main__":
    unittest.main()
