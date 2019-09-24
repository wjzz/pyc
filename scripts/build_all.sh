for file in examples/*.sil
do 
    echo $file
    ./scripts/compile.sh $file 
done
