# compiles all examples and stores the contents written to stdout in .output files for later comparison

for file in examples/*.sil
do 
    echo $file
    filename=`basename "$file"`
    base=`basename "$file" .sil`    # part without the extension
    (./scripts/compile.sh $file > /dev/null && ./target/$base >examples/outputs/$base.output) \
      || echo "ERROR: $file"
done

