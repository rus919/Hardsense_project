import csv

states = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0', '-', '_']
#states = ['1','2','3','4','5','6','7','8','9','0']
# states = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y']

n = 3
filename = 'only.csv'

def increment(arr):
    last = n - 1
    cut_off = len(states) - 1

    arr[last] += 1

    for i in range(last, 0, -1):
        if arr[i] > cut_off:
            arr[i] = 0
            arr[i - 1] += 1
        else:
            break
    return arr


def permutations(states, n):
    if len(states) <= 1: return
    if n == 0: return

    current = [0] * n

    out = []
    count = 0

    possibilities = len(states) ** n

    while count < possibilities:
        new_permutation = []

        for i in range(0, n):
            j = current[i]
            new_permutation += [states[j]]
        out += [new_permutation]

        count += 1
        current = increment(current)

    return out

def write_file(filename,permutations):
    listFile = open(filename, 'w+')
    writer = csv.writer(listFile)

    for item in permutations:
        word = ''.join(item)
        writer.writerow([word])

print(permutations(states, n))

def main():
    words = permutations(states, n)
    write_file(filename,words)


if __name__ == '__main__':
    main()