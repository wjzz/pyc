.PHONY:  test unit e2e test-errors cov cov-unit cov-e2e lint format typecheck pedantic std primes
.SILENT: test unit e2e test-errors cov cov-unit cov-e2e lint format typecheck pedantic std primes

CODE_DIR = src

test: unit e2e test-errors

unit:
	echo "Running unit tests...\n"
	$(MAKE) -s test -C $(CODE_DIR)

e2e:
	echo "Running e2e tests..."
	./scripts/test_all.sh

test-errors:
	echo "Running e2e tests on incorrect inputs..."
	./scripts/test_errors.sh

cov:
	clear
	echo "Generating test coverage info for the whole test suite...\n"
	$(MAKE) -s coverage -C $(CODE_DIR)

cov-unit:
	clear
	echo "Generating test coverage info for unit tests...\n"
	$(MAKE) -s coverage-unit -C $(CODE_DIR)

cov-e2e:
	clear
	echo "Generating test coverage info for e2e tests...\n"
	$(MAKE) -s coverage-e2e -C $(CODE_DIR)

pedantic: format lint typecheck

format:
	@echo "Formatting the code using black...\n"
	@python -m black -t py38 --exclude tests.py src

lint:
	echo "Generating linting information...\n"
	python -m flake8 --exclude tests.py,optimize.py --max-line-length 88 src

typecheck:
	echo "Typechecking the python source files...\n"
	#echo "Mypy"
	#python -m mypy src
	#mypy src
	echo "Pyright"
	pyright -p src

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
