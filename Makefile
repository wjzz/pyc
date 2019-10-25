.PHONY: std primes test e2e cov-unit cov-e2e
.SILENT: test e2e cov-unit cov-e2e

CODE_DIR = src

test:
	clear
	echo "Running unit tests...\n"
	$(MAKE) -s test -C $(CODE_DIR)

e2e:
	clear
	echo "Running e2e tests..."
	./scripts/test_all.sh

cov-unit:
	clear
	echo "Generating test coverage info for unit tests...\n"
	$(MAKE) -s coverage-unit -C $(CODE_DIR)

cov-e2e:
	clear
	echo "Generating test coverage info for e2e tests...\n"
	$(MAKE) -s coverage-e2e -C $(CODE_DIR)

std:
	# NOTE: this contains debugging flags
	nasm -f elf64 -g -o std.o std.asm -l std.lst
	ld -g -o std std.o

primes:
	nasm -f elf64 -o prime.o primes.asm \
	&& ld -o prime prime.o \
        && rm prime.o

## Examples for eventual use

hello:
	nasm -f elf64 -o hello.o hello5.asm
        # gcc will include libc by default, by the initial section must be 
        # called main
	gcc -Wall -Wextra -Werror -o hello hello.o
        # ld -o hello hello.o -lc -I /lib/x86_64-linux-gnu/libc.so.6

dynamic:
	nasm -f elf64 -o hello.o hello5.asm
	ld -o hello hello.o -lc --dynamic-linker\
	 /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 
