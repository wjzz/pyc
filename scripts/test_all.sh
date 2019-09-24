# compiles all examples and compares the contents from corresponding .output files

for file in examples/*.sil
do 
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    (./scripts/compile.sh $file > /dev/null && ./target/$base >tmpfile && diff tmpfile examples/outputs/$base.output) \
      || echo "ERROR: $file"
done
rm -f tmpfile

