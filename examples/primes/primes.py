limit = 1000000
count = 0
current = 2
while current <= limit:
    is_prime = 1
    if current != 2 and current % 2 == 0:
        is_prime = 0
    candidate = 3
    while is_prime == 1 and candidate * candidate <= current:
        if current % candidate == 0:
            is_prime = 0
        candidate += 1
    if is_prime == 1:
        #print(current)
        count += 1
    current += 1
print("Total =", count)
