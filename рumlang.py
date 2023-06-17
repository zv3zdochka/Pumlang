import time


def nth_prime(n):
    prime_count = 0
    num = 1

    while prime_count < n:
        num += 1
        is_prime = True

        i = 2
        while i * i <= num:
            if num % i == 0:
                is_prime = False
                break
            i += 1

        if is_prime:
            prime_count += 1
    return num

n = int(input())
print(nth_prime(n))

