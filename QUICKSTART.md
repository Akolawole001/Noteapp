# Quick Start Guide

## Running the Calculator

There are three ways to run the calculator:

### Method 1: Using the launcher script (Recommended)
```bash
./calc.py
```

### Method 2: Using Python module
```bash
python3 -m calculator.main
```

### Method 3: Direct execution
```bash
./calculator/main.py
```

## First Steps

Once you start the calculator, you'll see:
```
╔════════════════════════════════════════════════════════════╗
║        Scientific Calculator - Terminal Edition            ║
║                Production-Grade v1.0                       ║
╚════════════════════════════════════════════════════════════╝
```

The prompt will show:
```
calc>
```

## Try These Examples

### Basic Arithmetic
```
calc> 2 + 2
  = 4.0

calc> 10 - 3
  = 7.0

calc> 4 * 5
  = 20.0

calc> 20 / 4
  = 5.0

calc> 2 ^ 8
  = 256.0
```

### Using Parentheses
```
calc> (2 + 3) * 4
  = 20.0

calc> 2 + (3 * 4)
  = 14.0
```

### Square Root and Powers
```
calc> sqrt(16)
  = 4.0

calc> sqrt(2)
  = 1.4142135623730951

calc> 3^2 + 4^2
  = 25.0
```

### Trigonometry (Radians Mode - Default)
```
calc> sin(0)
  = 0.0

calc> cos(0)
  = 1.0

calc> sin(pi/2)
  = 1.0

calc> tan(pi/4)
  = 0.9999999999999999
```

### Trigonometry (Degrees Mode)
```
calc> degrees
Angle mode: degrees

calc> sin(90)
  = 1.0

calc> cos(180)
  = -1.0

calc> radians
Angle mode: radians
```

### Logarithms
```
calc> log10(100)
  = 2.0

calc> log10(1000)
  = 3.0

calc> ln(e)
  = 1.0

calc> log2(8)
  = 3.0

calc> log(100, 10)
  = 2.0
```

### Using Constants
```
calc> pi
  = 3.141592653589793

calc> e
  = 2.718281828459045

calc> 2 * pi
  = 6.283185307179586

calc> e^2
  = 7.3890560989306495
```

### Complex Expressions
```
calc> sqrt(sin(pi/2)^2 + cos(0)^2)
  = 1.4142135623730951

calc> log10(100) + sqrt(16)
  = 6.0

calc> (3 + 4) * (5 - 2)
  = 21.0
```

## Commands

### Get Help
```
calc> help
```

### List All Functions
```
calc> functions
```

### List All Constants
```
calc> constants
```

### Check Current Angle Mode
```
calc> mode
Current angle mode: radians
```

### Exit Calculator
```
calc> quit
```
or
```
calc> exit
```
or press `Ctrl+D`

## Error Handling

The calculator provides helpful error messages:

### Division by Zero
```
calc> 1/0
Evaluation error: Division by zero
```

### Invalid Function
```
calc> unknown(5)
Evaluation error: Unknown or disallowed function: unknown
```

### Syntax Error
```
calc> 2 + + 3
Syntax error: Expected EOF, got PLUS
```

### Domain Error
```
calc> sqrt(-1)
Evaluation error: Square root of negative number: -1.0

calc> log10(-5)
Evaluation error: log10 domain error: -5 <= 0
```

## Tips and Tricks

1. **Whitespace doesn't matter**: `2+2` and `2 + 2` are the same

2. **Use parentheses**: When in doubt, use parentheses to make order of operations clear

3. **Case-insensitive functions**: `SIN(0)`, `sin(0)`, and `Sin(0)` all work

4. **Experiment**: The calculator won't crash, so try things out!

5. **Check available functions**: Use the `functions` command to see what's available

6. **Multiple arguments**: Some functions like `log(value, base)` and `atan2(y, x)` take multiple arguments

## Running Tests

To verify the calculator is working correctly:

```bash
pytest calculator/tests/ -v
```

You should see all tests passing:
```
test_lexer.py::TestLexer::test_single_number PASSED
test_lexer.py::TestLexer::test_float_number PASSED
test_parser.py::TestParser::test_simple_number PASSED
test_parser.py::TestParser::test_addition PASSED
test_eval.py::TestEvaluator::test_addition PASSED
...
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the correct directory:
```bash
cd /Users/implicity/kola-repo
python3 -m calculator.main
```

### Python Version
Ensure you have Python 3.10 or higher:
```bash
python3 --version
```

## Next Steps

1. Try all the example expressions above
2. Experiment with nested functions
3. Mix constants with operations
4. Read the full README.md for more details
5. Explore the code in the calculator/ directory

Happy calculating! 🧮
