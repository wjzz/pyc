filename=`basename "$1"`
base=`basename "$1" .sil`    # part without the extension
target="target/"
# echo "filename = $filename"
# echo "base = $base"

mkdir -p $target

echo -n "Compiling the program... "
python3.7 -B src/main.py $1 > $target$base.asm \
  && echo "OK!" \
  && echo -n "Running the assembler... " \
  && nasm -f elf64 -o $target$base.o $target$base.asm \
  && echo "OK!" \
  && echo -n "Running the linker... " \
  && ld -o $target$base $target$base.o \
  && echo "OK!" \
  && echo "Running the program... " \
  && ./$target$base
  echo "Return value = $?"
