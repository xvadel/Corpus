import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  runApp(const CalculatorApp());
}

class CalculatorApp extends StatelessWidget {
  const CalculatorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calculator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        fontFamily: 'SF Pro Display',
        useMaterial3: true,
      ),
      home: const CalculatorScreen(),
    );
  }
}

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({super.key});

  @override
  State<CalculatorScreen> createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  String _display = '0';
  String _equation = '';
  double _firstOperand = 0;
  String _operator = '';
  bool _shouldReset = false;

  void _onDigitPress(String digit) {
    setState(() {
      if (_shouldReset || _display == '0') {
        _display = digit;
        _shouldReset = false;
      } else {
        if (_display.length < 12) {
          _display += digit;
        }
      }
    });
  }

  void _onDecimalPress() {
    setState(() {
      if (_shouldReset) {
        _display = '0.';
        _shouldReset = false;
      } else if (!_display.contains('.')) {
        _display += '.';
      }
    });
  }

  void _onOperatorPress(String op) {
    setState(() {
      if (_operator.isNotEmpty && !_shouldReset) {
        _calculate();
      }
      _firstOperand = double.parse(_display);
      _operator = op;
      _equation = '${_formatNumber(_firstOperand)} $op';
      _shouldReset = true;
    });
  }

  void _calculate() {
    if (_operator.isEmpty) return;
    double secondOperand = double.parse(_display);
    double result = 0;

    switch (_operator) {
      case '+':
        result = _firstOperand + secondOperand;
        break;
      case '−':
        result = _firstOperand - secondOperand;
        break;
      case '×':
        result = _firstOperand * secondOperand;
        break;
      case '÷':
        result = secondOperand != 0 ? _firstOperand / secondOperand : 0;
        break;
    }

    setState(() {
      _display = _formatNumber(result);
      _equation = '';
      _operator = '';
      _shouldReset = true;
    });
  }

  void _onEquals() {
    _calculate();
  }

  void _onClear() {
    setState(() {
      _display = '0';
      _equation = '';
      _firstOperand = 0;
      _operator = '';
      _shouldReset = false;
    });
  }

  void _onToggleSign() {
    setState(() {
      if (_display != '0') {
        if (_display.startsWith('-')) {
          _display = _display.substring(1);
        } else {
          _display = '-$_display';
        }
      }
    });
  }

  void _onPercent() {
    setState(() {
      double val = double.parse(_display);
      _display = _formatNumber(val / 100);
    });
  }

  String _formatNumber(double number) {
    if (number == number.toInt().toDouble() && !number.isInfinite && !number.isNaN) {
      return number.toInt().toString();
    }
    String str = number.toStringAsFixed(8);
    str = str.replaceAll(RegExp(r'0+$'), '');
    if (str.endsWith('.')) str = str.substring(0, str.length - 1);
    return str;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF1a1a2e), Color(0xFF16213e), Color(0xFF0f3460)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Display area
              Expanded(
                flex: 2,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                  alignment: Alignment.bottomRight,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      if (_equation.isNotEmpty)
                        Text(
                          _equation,
                          style: TextStyle(
                            fontSize: 22,
                            color: Colors.white.withOpacity(0.5),
                          ),
                        ),
                      const SizedBox(height: 8),
                      FittedBox(
                        fit: BoxFit.scaleDown,
                        alignment: Alignment.centerRight,
                        child: Text(
                          _display,
                          style: const TextStyle(
                            fontSize: 72,
                            fontWeight: FontWeight.w200,
                            color: Colors.white,
                            letterSpacing: 2,
                          ),
                          maxLines: 1,
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              // Divider
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 20),
                height: 1,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.white.withOpacity(0),
                      Colors.white.withOpacity(0.3),
                      Colors.white.withOpacity(0),
                    ],
                  ),
                ),
              ),

              // Buttons area
              Expanded(
                flex: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      _buildRow(['AC', '+/-', '%', '÷']),
                      const SizedBox(height: 12),
                      _buildRow(['7', '8', '9', '×']),
                      const SizedBox(height: 12),
                      _buildRow(['4', '5', '6', '−']),
                      const SizedBox(height: 12),
                      _buildRow(['1', '2', '3', '+']),
                      const SizedBox(height: 12),
                      _buildBottomRow(),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRow(List<String> labels) {
    return Expanded(
      child: Row(
        children: labels.map((label) {
          return Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6),
              child: _buildButton(label),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildBottomRow() {
    return Expanded(
      child: Row(
        children: [
          Expanded(
            flex: 2,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6),
              child: _buildButton('0', flex: 2),
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6),
              child: _buildButton('.'),
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6),
              child: _buildButton('='),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildButton(String label, {int flex = 1}) {
    final isOperator = ['÷', '×', '−', '+', '='].contains(label);
    final isUtility = ['AC', '+/-', '%'].contains(label);

    Color bgColor;
    Color textColor;

    if (isOperator) {
      bgColor = const Color(0xFFe94560);
      textColor = Colors.white;
    } else if (isUtility) {
      bgColor = Colors.white.withOpacity(0.15);
      textColor = Colors.white;
    } else {
      bgColor = Colors.white.withOpacity(0.08);
      textColor = Colors.white;
    }

    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => _onButtonPress(label),
        borderRadius: BorderRadius.circular(20),
        splashColor: Colors.white.withOpacity(0.2),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          decoration: BoxDecoration(
            color: bgColor,
            borderRadius: BorderRadius.circular(20),
            boxShadow: isOperator
                ? [
                    BoxShadow(
                      color: const Color(0xFFe94560).withOpacity(0.4),
                      blurRadius: 12,
                      offset: const Offset(0, 4),
                    ),
                  ]
                : [],
          ),
          child: Center(
            child: Text(
              label,
              style: TextStyle(
                fontSize: isUtility ? 20 : 28,
                fontWeight: FontWeight.w400,
                color: textColor,
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _onButtonPress(String label) {
    HapticFeedback.lightImpact();
    switch (label) {
      case 'AC':
        _onClear();
        break;
      case '+/-':
        _onToggleSign();
        break;
      case '%':
        _onPercent();
        break;
      case '.':
        _onDecimalPress();
        break;
      case '=':
        _onEquals();
        break;
      case '+':
      case '−':
      case '×':
      case '÷':
        _onOperatorPress(label);
        break;
      default:
        _onDigitPress(label);
    }
  }
}
