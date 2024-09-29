import sys

# The part surrounded in dashes is only included because translator.test.py is
# mistakenly searching for a 'test' module in translator, because of the odd
# naming convention of the test folder. Since, we were given explicit orders
# not to change the test folder, I had to add a 'test' class, so that it runs the
# contents there instead. The contents are identical though.
# ------------------------------------------------------------------------------
import unittest
import subprocess
class test(unittest.TestCase):
    def test_output(self):
        # Command to run translator.py script
        command = ["python3", "translator.py", "Abc", "123", "xYz"]

        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)

        # Expected output without the newline at the end
        expected_output = ".....OO.....O.O...OO...........O.OOOO.....O.O...OO..........OO..OO.....OOO.OOOO..OOO"
        # Strip any leading/trailing whitespace from the output and compare
        self.assertEqual(result.stdout.strip(), expected_output)

# ------------------------------------------------------------------------------

# special brailles. need to check these

capital_follows = ".....O"
decimal_follows = ".O...O"  # This probably is to differentiate from periods and decimal points
number_follows = ".O.OOO"
space = "......"  # perhaps, could just add this in the dictionary

# Note: O and > have the same braille ???

# For now, I just excluded the > character in the conversion

# Use for braille conversion
braille_to_chars = {"O.....": "a", "O.O...": "b","OO....": "c","OO.O..": "d","O..O..": "e","OOO...": "f","OOOO..": "g","O.OO..": "h",".OO...": "i",".OOO..": "j","O...O.":"k", "O.O.O.":"l","OO..O.":"m","OO.OO.":"n","O..OO.":"o","OOO.O.":"p","OOOOO.":"q","O.OOO.":"r",".OO.O.":"s",".OOOO.":"t","O...OO":"u","O.O.OO":"v",".OOO.O":"w","OO..OO":"x","OO.OOO":"y","O..OOO":"z","..OO.O":".","..O...":",","..O.OO":"?","..OOO.":"!","..OO..":":","..O.O.":";","....OO":"-",".O..O.":"/",".OO..O":"<","O.O..O":"(",".O.OO.":")"}
braille_to_numbers = {"O.....": "1", "O.O...": "2","OO....": "3","OO.O..": "4","O..O..": "5","OOO...": "6","OOOO..": "7","O.OO..": "8",".OO...": "9",".OOO..": "0"}

# Use for sentence conversion
chars_to_braille = {'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..', 'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..', 'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.', 'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.', 'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO', 'y': 'OO.OOO', 'z': 'O..OOO', '.': '..OO.O', ',': '..O...', '?': '..O.OO', '!': '..OOO.', ':': '..OO..', ';': '..O.O.', '-': '....OO', '/': '.O..O.', '<': '.OO..O','(': 'O.O..O', ')': '.O.OO.'}
numbers_to_braille = {'1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..', '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...', '0': '.OOO..'}


# Function to translate Braille to English
def braille_to_text(braille_input): # this part works

    is_number = False
    is_capital = False

    text_output = ""
    braille_chars = [braille_input[i: i+6] for i in range(0, len(braille_input), 6)]

    for char in braille_chars:
        if char == capital_follows:
            is_capital = True
        elif char == decimal_follows:
            is_capital = False  # Don't know what to do in this case
            pass
        elif char == number_follows:
            is_number = True
            is_capital = False
        elif char == space:
            is_number = False
            is_capital = False
            text_output += " "
            pass
        else:
            if is_number:
                text_output += braille_to_numbers[char]
            elif is_capital:
                text_output += braille_to_chars[char].upper()
                is_capital = False
            else:
                text_output += braille_to_chars[char]
                is_capital = False

    return text_output


# Function to translate English to Braille
def text_to_braille(text_input):

    braille_output = ""
    is_number = False

    for char in text_input:
        if char.isupper():
            if is_number:  # If we were processing numbers, reset
                is_number = False
            braille_output += capital_follows
            braille_output += chars_to_braille[char.lower()]
        elif char.isdigit():
            if not is_number:
                braille_output += number_follows  # Only prepend this once
                is_number = True
            braille_output += numbers_to_braille[char]
        elif char == " ":
            if is_number:  # Reset number mode on spaces
                is_number = False
            braille_output += space
        else:
            if is_number:  # If we were processing numbers, reset
                is_number = False
            braille_output += chars_to_braille[char]

    return braille_output

# Function to determine input type and translate accordingly
def translate(input_str):
    if is_braille(input_str):
        return braille_to_text(input_str)
    else:
        return text_to_braille(input_str)

# Helper function to check if input is Braille
def is_braille(input_str):
    # Check if the string contains 'O' and '.'
    return all(c in 'O.' for c in input_str) and len(input_str) % 6 == 0# might have to add the condition that len(input_str) % 6 == 0


if __name__ == "__main__":

    input_str = ""

    if len(sys.argv) == 1:  # if user doesnt provide any arguments
        print("Incorrect Usage")
    elif len(sys.argv) == 2: # if user provides one argument (could be brail)
        input_str = sys.argv[1]
    else: # if user provides more than one argument (cannot be brail. its just spaces)
        input_str = " ".join(sys.argv[1:]).strip()

    result = translate(input_str)
    print(result)
