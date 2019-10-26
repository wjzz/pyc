#!/bin/bash

# compiles all examples and compares the contents from corresponding .output files

exit_code=0  # all OK

for file in examples/*.sil
do 
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    ./scripts/compile.sh $file > /dev/null && ./target/$base >tmpfile && diff tmpfile examples/outputs/$base.output
    if [ $? -ne 0 ]
    then
      exit_code=1
      echo "ERROR: $file"
    fi
done
rm -f tmpfile

exit $exit_code
