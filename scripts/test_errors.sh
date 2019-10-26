#!/bin/bash

# compiles all examples and makes sure the exit code is 1 (EXIT_FAILURE)

exit_code=0  # all tests OK

for file in errors/*.sil
do
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    python src/main.py $file > /dev/null 2> /dev/null
    if [ $? -ne 1 ]
    then
      exit_code=1
      echo "NO ERROR FOUND FOR INCORRENT FILE: $file"
    fi
done
rm -f tmpfile

exit $exit_code
