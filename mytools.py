import hashlib
P = 500000
num_file = 1000
Htable = []
word_space = []

with open('index_test', 'r') as f:
    for line in f:
        if num_file == 0:
            break
        num_file -= 1
        temp = line.strip('\n').split(' ')
        word_space.append(temp[1:])
        for word in temp[1:]:
            if word not in Htable:
                Htable.append(word)
def hs(w):
    #return int.from_bytes(hashlib.sha256(bytes(w, encoding='utf-8')).digest(), byteorder='little')%P
    #return sum([ord(ch) for ch in w])
    # if w not in Htable:
    #     return int.from_bytes(hashlib.sha256(bytes(w, encoding='utf-8')).digest(), byteorder='little')%P + len(Htable)
    # return (Htable.index(w)+1)
    return int.from_bytes(hashlib.sha256(bytes(w, encoding='utf-8')).digest(), byteorder='little')%P

if __name__ == '__main__':
    s = set()
    for word in Htable:
        s.add(hs(word))
    print(len(Htable), len(s))