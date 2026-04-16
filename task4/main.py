import sys


# ---------------------------------------------------------------------------
# Conversion functions
# ---------------------------------------------------------------------------

def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c: float) -> float:
    return c + 273.15


def kelvin_to_celsius(k: float) -> float:
    return k - 273.15


def fahrenheit_to_kelvin(f: float) -> float:
    return celsius_to_kelvin(fahrenheit_to_celsius(f))


def kelvin_to_fahrenheit(k: float) -> float:
    return celsius_to_fahrenheit(kelvin_to_celsius(k))


CONVERSIONS: dict[str, tuple[str, str, callable]] = {
    "1": ("Celsius",    "Fahrenheit", celsius_to_fahrenheit),
    "2": ("Fahrenheit", "Celsius",    fahrenheit_to_celsius),
    "3": ("Celsius",    "Kelvin",     celsius_to_kelvin),
    "4": ("Kelvin",     "Celsius",    kelvin_to_celsius),
    "5": ("Fahrenheit", "Kelvin",     fahrenheit_to_kelvin),
    "6": ("Kelvin",     "Fahrenheit", kelvin_to_fahrenheit),
}

UNITS = {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}

ABSOLUTE_ZERO = {"Celsius": -273.15, "Fahrenheit": -459.67, "Kelvin": 0.0}

MENU = """
╔════════════════════════════════╗
║    Temperature Converter       ║
╠════════════════════════════════╣
║  1. Celsius    → Fahrenheit    ║
║  2. Fahrenheit → Celsius       ║
║  3. Celsius    → Kelvin        ║
║  4. Kelvin     → Celsius       ║
║  5. Fahrenheit → Kelvin        ║
║  6. Kelvin     → Fahrenheit    ║
║  7. Exit                       ║
╚════════════════════════════════╝
"""


def read_temperature(prompt: str, unit: str) -> float:
    """Read and validate a temperature value, enforcing physical lower bound."""
    min_val = ABSOLUTE_ZERO[unit]
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
        except ValueError:
            print(f"  ✗ Please enter a numeric value.\n")
            continue
        if val < min_val:
            sym = UNITS[unit]
            print(
                f"  ✗ {val}{sym} is below absolute zero "
                f"({min_val}{sym} for {unit}). Try again.\n"
            )
            continue
        return val


def main() -> None:
    print(MENU)
    while True:
        choice = input("Select conversion (1-7): ").strip()

        if choice == "7":
            print("\nGoodbye!")
            sys.exit(0)

        if choice not in CONVERSIONS:
            print("  ✗ Invalid choice. Enter 1-7.\n")
            continue

        from_unit, to_unit, convert_fn = CONVERSIONS[choice]
        from_sym = UNITS[from_unit]
        to_sym = UNITS[to_unit]

        value = read_temperature(
            f"  Enter temperature in {from_unit} ({from_sym}): ", from_unit
        )
        result = convert_fn(value)

        print(f"\n  ✓ {value:.4g}{from_sym}  =  {result:.4f}{to_sym}\n")
        input("Press Enter to return to menu...")
        print(MENU)


if __name__ == "__main__":
    main()
