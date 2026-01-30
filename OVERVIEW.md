# 🧮 Terminal Scientific Calculator - Production Ready

## Overview

A fully-functional, production-grade terminal-only scientific calculator built following enterprise software architecture principles. This project demonstrates clean code, security-first design, and comprehensive testing.

## Quick Start

### Run the Calculator
```bash
./calc.py
```

### Try It Out
```
calc> 2 + 2
  = 4.0

calc> sqrt(16) + log10(100)
  = 6.0

calc> sin(pi/2)
  = 1.0

calc> quit
Goodbye!
```

## Project Stats

- **Total Code**: ~1,691 lines of Python
- **Modules**: 20 files organized in 7 layers
- **Tests**: 53 comprehensive test cases
- **Functions**: 25+ mathematical functions
- **Security**: 5 layers of protection

## Architecture

```
Terminal Input
    ↓
CLI Layer (REPL)
    ↓
Lexer (Tokenization)
    ↓
Parser (AST Generation)
    ↓
Evaluator (Computation)
    ↓
Math Library (Pure Functions)
```

## Key Features

### ✅ Mathematical Operations
- Basic arithmetic: `+`, `-`, `*`, `/`, `^`
- Scientific functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `ln`, `exp`
- Constants: `pi`, `e`, `tau`, `phi`
- Angle modes: radians and degrees

### ✅ Security Controls
- No `eval()` - expressions are parsed and validated
- Function whitelisting - only approved operations
- Input limits - prevents resource exhaustion
- Timeout protection - 5-second execution limit
- Depth limits - prevents stack overflow

### ✅ Production Quality
- Layered architecture with separation of concerns
- Comprehensive error handling
- Type hints throughout
- Full test coverage
- Clear documentation

## File Structure

```
calculator/
├── cli/              # User interface
│   └── repl.py       # Interactive REPL
├── core/             # Core processing
│   ├── ast.py        # AST nodes
│   ├── lexer.py      # Tokenizer
│   ├── parser.py     # Parser
│   └── evaluator.py  # Evaluator
├── mathlib/          # Math functions
│   ├── arithmetic.py # Basic ops
│   ├── trig.py       # Trig functions
│   ├── logs.py       # Logarithms
│   └── constants.py  # Constants
├── security/         # Security controls
│   └── limits.py     # Safety limits
├── tests/            # Test suite
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_eval.py
└── main.py           # Entry point
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - User guide with examples
- **[calculator/README.md](calculator/README.md)** - Full documentation
- **[BUILD_SUMMARY.md](BUILD_SUMMARY.md)** - Implementation details
- **[Calculator.md](Calculator.md)** - Architecture specification

## Testing

### Run Tests
```bash
pytest calculator/tests/ -v
```

### Quick Verification
```bash
python3 test_calculator.py
```

Expected output:
```
✓ 2 + 2                = 4.0
✓ sqrt(16)             = 4.0
✓ log10(100)           = 2.0
✅ Calculator is working correctly!
```

## Usage Examples

### Basic Math
```
calc> 2 + 2
  = 4.0

calc> (3 + 4) * 2
  = 14.0
```

### Scientific Functions
```
calc> sqrt(16)
  = 4.0

calc> log10(1000)
  = 3.0

calc> exp(0)
  = 1.0
```

### Trigonometry
```
calc> sin(0)
  = 0.0

calc> degrees
Angle mode: degrees

calc> sin(90)
  = 1.0
```

### Using Constants
```
calc> pi
  = 3.141592653589793

calc> 2 * pi
  = 6.283185307179586

calc> e^2
  = 7.3890560989306495
```

## Why Production-Grade?

### 1. **Security**
- Never executes arbitrary code
- Multiple layers of validation
- Resource limits prevent abuse
- Graceful error handling

### 2. **Architecture**
- Clean separation of concerns
- Each module has single responsibility
- Easy to test and maintain
- Extensible design

### 3. **Quality**
- Comprehensive test coverage
- Type hints for clarity
- Clear error messages
- Professional code structure

### 4. **Documentation**
- Multiple guides for different audiences
- Code comments and docstrings
- Architecture documentation
- Usage examples

## Available Commands

| Command | Description |
|---------|-------------|
| `help` | Show help message |
| `functions` | List all available functions |
| `constants` | List all available constants |
| `radians` | Switch to radians mode |
| `degrees` | Switch to degrees mode |
| `mode` | Show current angle mode |
| `quit` / `exit` | Exit calculator |

## Development

### Running Tests
```bash
# All tests
pytest calculator/tests/ -v

# Specific test file
pytest calculator/tests/test_parser.py -v

# With coverage
pytest calculator/tests/ --cov=calculator
```

### Adding New Functions

1. Add function to appropriate mathlib module
2. Register in `ALLOWED_FUNCTIONS` in evaluator.py
3. Add tests
4. Update documentation

## Error Handling

The calculator provides clear, helpful error messages:

```
calc> 1/0
Evaluation error: Division by zero

calc> sqrt(-1)
Evaluation error: Square root of negative number: -1.0

calc> unknown(5)
Evaluation error: Unknown or disallowed function: unknown
```

## Requirements

- Python 3.10 or higher
- No external dependencies for running
- pytest for testing (optional)

## Implementation Highlights

### Lexer
- Tokenizes input safely
- Rejects invalid characters immediately
- Tracks position for error messages

### Parser
- Recursive descent with operator precedence
- Right-associative power operator
- Comprehensive error detection

### Evaluator
- Walks AST to compute results
- Function whitelisting
- Domain validation

### Math Library
- Pure functions (no side effects)
- Comprehensive coverage
- Domain error checking

### Security
- Input sanitization
- Expression length limits
- Recursion depth limits
- Timeout protection

## Future Enhancements

Potential additions:
- Complex number support
- Matrix operations
- Statistical functions
- User-defined variables
- Expression history
- Unit conversions

## Conclusion

This calculator demonstrates how to build production-quality software with:
- **Clean architecture** for maintainability
- **Security controls** for safety
- **Comprehensive testing** for reliability
- **Clear documentation** for usability

Perfect as a learning project or foundation for more advanced calculators.

---

**Status**: ✅ Production Ready

**Built with**: Python 3, Clean Architecture, Test-Driven Development

**License**: Educational Project
