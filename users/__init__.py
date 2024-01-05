from string import ascii_lowercase


def alphabet_position(text):
    alp = ascii_lowercase
    res = []
    for l in text:
        if l in alp:
            res.append(str(alp.index(l)+1))
    return ' '.join(res)


print(alphabet_position('abcddde'))