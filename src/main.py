import ast
import parser
import compile
import symbol_table

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        #print("got file name =", sys.argv[1])
        try:
            with open(file_name, "r") as f:
                lines = "".join(f.readlines())
                # parse
                c = parser.parse_file(lines)
                # compile
                result = compile.compile_top(c)
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
                print(f"\tError on line {line}:{pos}", 
                    file=dest)
                print(f"\t{err.msg}", file=dest)
                sys.exit(1)
        except symbol_table.UnboundVariableError as err:
            with sys.stderr as dest:
                print("\n/Error/ Unbound variable:", file=dest)
                print(f"\t{err.var}", file=dest)
                sys.exit(1)
        except Exception as e:
            print("Got lines:\n\t", lines)
            print("Failed to compile the file", file=sys.stderr)
            print(f"Error: {e}")
            raise e
    else:
        print("usage:")
        print(f"{sys.argv[0]} filename")