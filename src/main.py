import ast
import parser
import compile

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #print("got file name =", sys.argv[1])
        with open(sys.argv[1], "r") as f:
            lines = "".join(f.readlines())
            try:
                c = parser.parse_stm(lines)
                result = compile.compile_top(c)
                print(result)
            except parser.ParseError as err:
                with sys.stderr as dest:
                    line = err.token.line
                    pos = err.token.offset
                    print("Parse Error:", file=dest)
                    print(f"\tError on line {line}:{pos}", 
                        file=dest)
                    print(f"\t{err.msg}", file=dest)
                    sys.exit(1)
            except Exception as e:
                print("Got lines:\n\t", lines)
                print("Failed to parse the file", file=sys.stderr)
                print(f"Error: {e}")
                raise e
    else:
        print("usage:")
        print(f"{sys.argv[0]} filename")