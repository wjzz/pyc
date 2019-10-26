#!/bin/bash

# compiles all examples and makes sure the exit code is 1 (EXIT_FAILURE)

exit_code=0  # all tests OK
all=0
passing=0
failing=0

for file in errors/*.sil
do
    ((all++))
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    python src/main.py $file >tmpfile 2>tmpfile
    if [ $? -ne 2 ]
    then
      ((failing++))
      exit_code=1
      echo "NO ERROR FOUND FOR INCORRECT FILE: $file"
      cat tmpfile
    else
      ((passing++))
    fi
done
rm -f tmpfile

echo "Passed $passing/$all tests. Failed $failing tests."
exit $exit_code
