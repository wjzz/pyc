#include <stdio.h>

int main(void){
    long long limit = 1000000;
    long long count = 0;
    long long current = 2;
    while (current <= limit) {
        int is_prime = 1;
        if (current != 2 && current % 2 == 0){
            is_prime = 0;
        }
          
        long long cand = 3;
        while (is_prime == 1 && cand * cand <= current){
            if (current % cand == 0)
              is_prime = 0;
            cand++;
        }
        if (is_prime == 1)
            ++count;
        ++current;
    }
    printf("Total = %lld\n", count);
}