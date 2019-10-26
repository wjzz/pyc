#!/bin/bash

# compiles all examples and makes sure the exit code is 1 (EXIT_FAILURE)

exit_code=0  # all tests OK

for file in errors/*.sil
do
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    python src/main.py $file >tmpfile 2>tmpfile
    if [ $? -ne 2 ]
    then
      exit_code=1
      echo "NO ERROR FOUND FOR INCORRENT FILE: $file"
      cat tmpfile
    fi
done
rm -f tmpfile

exit $exit_code
