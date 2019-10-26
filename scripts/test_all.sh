#!/bin/bash

# compiles all examples and compares the contents from corresponding .output files

exit_code=0  # all OK
all=0
passing=0
failing=0

for file in examples/*.sil
do
    ((all++))
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    ./scripts/compile.sh $file > /dev/null && ./target/$base >tmpfile && diff tmpfile examples/outputs/$base.output
    if [ $? -ne 0 ]
    then
      ((failing++))
      exit_code=1
      echo "ERROR: $file"
    else
      ((passing++))
    fi
done
rm -f tmpfile

echo "Passed $passing/$all tests. Failed $failing tests."
exit $exit_code
