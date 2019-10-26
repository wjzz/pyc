"""
The main entry of the compiler.

This module is putting everything together, the file is:
- read
- parsed
- compiled
and then the generated assembly is printed out.
"""

import sys
import traceback

import parser
import type_checker
import code_generator

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            # print("got file name =", sys.argv[1])
            try:
                with open(file_name, "r") as f:
                    lines = "".join(f.readlines())
                    # parse
                    c = parser.parse_file(lines)
                    # type check
                    symbol_table = type_checker.check(c)
                    # compile
                    result = code_generator.compile_top(c)
                    # output
                    print(result)
            except FileNotFoundError:
                with sys.stderr as dest:
                    print("\n/Error/ File not found:", file=dest)
                    print(f"\t{file_name}", file=dest)
                    sys.exit(1)
            except parser.ParseError as err:
                with sys.stderr as dest:
                    line = err.token.line
                    pos = err.token.offset
                    print("\n/Error/ Parse Error:", file=dest)
                    print(f"\tError on line {line}:{pos}", file=dest)
                    print(f"\t{err.msg}", file=dest)
                    sys.exit(2)
            except type_checker.CTypeError as err:
                with sys.stderr as dest:
                    # TODO: add line information
                    print("\n/Error/ Type Error:", file=dest)
                    # print(f"\tError on line {line}:{pos}", file=dest)
                    print(f"\t{err.msg}", file=dest)
                    sys.exit(2)
            except NotImplementedError as e:
                print("Work in progress, NonImplmentedError", file=sys.stderr)
                print(f"Error: {e}", file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)
                sys.exit(1)
            except AssertionError as e:
                print("Work in progress, AssertionError", file=sys.stderr)
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            except Exception as e:
                print("Got lines:\n\t", lines)
                print("Failed to compile the file", file=sys.stderr)
                print(f"Error: {e}")
                raise e
    else:
        print("usage:")
        print(f"{sys.argv[0]} filename")
