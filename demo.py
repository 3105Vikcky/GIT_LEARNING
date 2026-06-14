#3ERJKMEKLFMRKLFNKLNF
#!/usr/bin/env python3
"""
Simple safe calculator CLI.

Usage:
  python demo.py
  python demo.py --test
"""
import ast
import operator as op
import sys

# Supported binary operators
OPERATORS = {
	ast.Add: op.add,
	ast.Sub: op.sub,
	ast.Mult: op.mul,
	ast.Div: op.truediv,
	ast.Pow: op.pow,
	ast.Mod: op.mod,
	ast.FloorDiv: op.floordiv,
}

# Supported unary operators
UNARY_OPERATORS = {
	ast.UAdd: lambda x: x,
	ast.USub: op.neg,
}


def eval_node(node):
	if isinstance(node, ast.Expression):
		return eval_node(node.body)
	if isinstance(node, ast.BinOp):
		left = eval_node(node.left)
		right = eval_node(node.right)
		oper = type(node.op)
		if oper in OPERATORS:
			return OPERATORS[oper](left, right)
		raise ValueError(f"Unsupported operator: {oper}")
	if isinstance(node, ast.UnaryOp):
		operand = eval_node(node.operand)
		oper = type(node.op)
		if oper in UNARY_OPERATORS:
			return UNARY_OPERATORS[oper](operand)
		raise ValueError(f"Unsupported unary operator: {oper}")
	if isinstance(node, ast.Num):  # Python <3.8
		return node.n
	if isinstance(node, ast.Constant):  # Python 3.8+
		if isinstance(node.value, (int, float)):
			return node.value
		raise ValueError("Only int/float constants are allowed")
	if isinstance(node, ast.Call):
		raise ValueError("Function calls are not allowed")
	raise ValueError(f"Unsupported expression: {type(node).__name__}")


def evaluate(expression):
	"""Evaluate an arithmetic expression safely and return the result."""
	tree = ast.parse(expression, mode="eval")
	return eval_node(tree)


def repl():
	print("Simple calculator. Type 'exit' or 'quit' to leave.")
	while True:
		try:
			s = input("calc> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not s:
			continue
		if s.lower() in ("exit", "quit"):
			break
		if s.lower() in ("help", "h", "?"):
			print("Enter arithmetic expressions using + - * / ** % // and parentheses.")
			continue
		try:
			result = evaluate(s)
			print(result)
		except Exception as e:
			print("Error:", e)


def run_tests():
	tests = {
		"1+2": 3,
		"2*3+4": 10,
		"2*(3+4)": 14,
		"2**3": 8,
		"-5+2": -3,
		"10/4": 2.5,
		"10//3": 3,
		"10%3": 1,
		"3+4*2/(1-5)**2": 3 + 4 * 2 / (1 - 5) ** 2,
	}
	for expr, expected in tests.items():
		got = evaluate(expr)
		assert got == expected, f"{expr} -> expected {expected}, got {got}"
	print("All tests passed.")


if __name__ == "__main__":
	if "--test" in sys.argv or "-t" in sys.argv:
		run_tests()
	else:
		repl()