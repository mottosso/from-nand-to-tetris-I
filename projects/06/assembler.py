#!/usr/bin/env python
"""
The Hack Assembler

Usage:
    $ assembler.py Add.asm
    Hack assembly successfully written to Add.hack

Compatible with Python 2.6+ and Python 3.x

"""

import re
import sys

# Globals
self = sys.modules[__name__]
self.next_available = 16

symbols = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 0x4000,
    "KBD": 0x6000,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}

dest = {
    None: "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

comp = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101"
}

# a=1
comp_a = {
    "M": comp["A"],
    "!M": comp["!A"],
    "-M": comp["-A"],
    "M+1": comp["A+1"],
    "M-1": comp["A-1"],
    "D+M": comp["D+A"],
    "D-M": comp["D-A"],
    "M-D": comp["A-D"],
    "D&M": comp["D&A"],
    "D|M": comp["D|A"]
}

comp.update(comp_a)

jump = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def _parser(iterable):
    """Parse an iterable object, typically a file

    Arguments:
        iterable (iter): File-like object, must support iteration

    Usage:
        >>> with open("some/file.asm") as f:
        ...   for command in _parser(f):
        ...     print(command)

    Yields:
        (dict) parsed commands

    """

    line_number = 0

    for line in iterable:
        line = line.strip()

        if not line or line.startswith("//"):
            continue

        line = line.split("//", 1)[0].rstrip()
        line = re.sub(" ", "", line)  # Remove spaces

        # Labels
        if re.findall(r"^\(.*\)$", line):
            label = line[1:-1]

            yield {
                "instruction": "label",
                "label": label,
                "line_number": line_number,
                "source": line
            }

        # A-instructions
        elif line.startswith("@"):
            symbol = line[1:]

            try:
                symbol = int(symbol)
            except ValueError:
                pass

            yield {
                "instruction": "a",
                "symbol": symbol,
                "line_number": line_number,
                "source": line
            }

            line_number += 1

        # C-instructions
        elif any(symbol in line for symbol in ("=", ";")):
            _, jump = (re.split(";", line) + [None])[:2]

            try:
                dest, comp = re.split("=", _)
            except ValueError:
                dest, comp = None, _

            yield {
                "instruction": "c",
                "dest": dest,
                "comp": comp,
                "jump": jump,
                "line_number": line_number,
                "source": line
            }

            line_number += 1

        else:
            raise SyntaxError("Unrecognised command: %s" % line)


def _translator(commands, verbose=False):
    """Assemble Hack Assembly commands into binary

    Arguments:
        commands (list): Dictionary of parsed command
        verbose (bool): Include original assembly alongside binary

    Usage:
        >>> for binary in _translator(commands):
        ...   print(binary)

    Yields:
        (str) Binary Hack instructions, e.g. "1110110101001"

    """

    for command in commands:
        instruction = command["instruction"]
        source = " // %s" % command["source"]

        if instruction == "a":
            symbol = command["symbol"]

            if not isinstance(symbol, int):
                symbol = symbols[symbol]

            value = bin(symbol)[2:].rjust(15, "0")
            yield "0{value}{source}".format(**{
                "value": value,
                "source": source if verbose else ""
            })

        elif instruction == "c":
            yield "111{a}{comp}{dest}{jump}{source}".format(**{
                "a": "1" if command["comp"] in comp_a else "0",
                "comp": comp[command["comp"]],
                "dest": dest[command["dest"]],
                "jump": jump[command.get("jump")],
                "source": source if verbose else ""
            })

        else:
            sys.stderr.write("Unknown command: %s" % command)


def assemble(file, verbose=False):
    """Assemble symbol and symbol-less Hack Assembly files

    Returns:
        (str): Resulting binary file

    """

    commands = list()
    output = list()

    # Parse file, as unintelligently as possible
    for command in _parser(file):
        commands.append(command)

    # Resolve labels first
    for command in commands:
        if command["instruction"] == "label":
            label = command["label"]
            line_number = command["line_number"]
            symbols[label] = line_number

    # Variables next
    for command in commands:
        if command["instruction"] == "a":
            symbol = command["symbol"]

            if isinstance(symbol, int):
                continue

            if symbol in symbols:
                continue

            address = self.next_available
            self.next_available += 1

            symbols[symbol] = address

    # Produce binary output
    for binary in _translator(commands, verbose):
        output.append(binary)

    return "\n".join(output) + "\n"


def test_parser_a_instructions():
    """A-instructions are parsed correctly"""
    for command in _parser(["@0",
                            "@1",
                            "@R1",
                            "@5500",
                            "@myVariable"
                            ]):
        assert command["instruction"] == "a"


def test_parser_a_instructions_int():
    """Symbol-less a-instructions are integers"""
    for command in _parser(["@0",
                            "@1",
                            "@123",
                            "@5500",
                            ]):
        assert command["instruction"] == "a"
        assert isinstance(command["symbol"], int)


def test_parser_c_instructions():
    """C-instructions are recognised correctly"""
    for command in _parser(["A=D",
                            "D=A",
                            "0;JMP",
                            "M=-1;JMP",
                            ]):
        assert command["instruction"] == "c"


def test_parser_destination_less():
    """C-instructions without destination are parsed correctly"""
    for command in _parser(["A;JMP",
                            "0;JMP",
                            ]):
        assert command["instruction"] == "c"
        assert command["dest"] is None


def test_parser_label():
    """Labels are correctly recognised"""
    for command in _parser(["(label1)",
                            "(102)",
                            ]):
        assert command["instruction"] == "label"
        assert isinstance(command["label"], str)


def test_compare_nosymbols():
    """Compare output of our assembler with theirs

    WARNING: This requires Assembler.sh to be on your PATH

    """

    import os
    import subprocess

    src = "add/Add.asm"
    compare = "add/Add.hack"

    if os.path.exists(compare):
        os.remove(compare)

    subprocess.call(["Assembler.sh", src])

    with open(compare) as f:
        theirs = f.read()

    os.remove(compare)

    with open(src) as f:
        ours = assemble(f)

    print(ours)
    print(theirs)
    assert ours == theirs


def test_compare_withsymbols():
    """Compare output of our assembler with theirs

    WARNING: This requires Assembler.sh to be on your PATH

    """

    import os
    import subprocess

    src = "max/Max.asm"
    compare = "max/Max.hack"

    if os.path.exists(compare):
        os.remove(compare)

    subprocess.call(["Assembler.sh", src])

    with open(compare) as f:
        theirs = f.read()

    os.remove(compare)

    with open(src) as f:
        ours = assemble(f)

    print(ours)
    print(theirs)
    assert ours == theirs


def test_compare_pong():
    """Compare output of our assembler with theirs

    WARNING: This requires Assembler.sh to be on your PATH

    """

    import os
    import subprocess

    src = "pong/Pong.asm"
    compare = "pong/Pong.hack"

    if os.path.exists(compare):
        os.remove(compare)

    subprocess.call(["Assembler.sh", src])

    with open(compare) as f:
        theirs = f.read()

    os.remove(compare)

    with open(src) as f:
        ours = assemble(f)

    print(ours)
    print(theirs)
    assert ours == theirs

if __name__ == '__main__':
    import os
    import time
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", "-o")
    parser.add_argument("--stdout", help="Write to stdout",
                        action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    src = os.path.abspath(args.input)
    if not os.path.exists(src):
        sys.stderr.write("%s was not found.\n" % src)

    if args.output:
        dst = os.path.abspath(args.output)
    else:
        dirname = os.path.dirname(src)
        basename = os.path.basename(args.input)
        name, ext = os.path.splitext(basename)
        dst = os.path.join(dirname, name + ".hack")

    _start = time.time()
    with open(src) as f:
        output = assemble(f, verbose=args.verbose)

    if not args.stdout:
        with open(dst, "w") as f:
            f.write(output)
    else:
        sys.stdout.write(output)

    _end = time.time()
    sys.stdout.write("Hack assembly successfully "
                     "written to Add.hack in %.2fms\n"
                     % ((_end - _start) * 1000))
