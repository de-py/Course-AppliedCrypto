import rypto


a = '69 73 20 74 68 69 73 20 68 65 61 76 65 6e'.replace(' ','')

b = "6e 6f 20 69 74 27 73 20 69 6f 77 61 21 21".replace(' ','')


c = rypto.h2bin(a)

d = rypto.h2bin(b)

print rypto.ham(c,d)


