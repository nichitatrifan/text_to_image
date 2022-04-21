import string

if __name__=='__main__':
    c_list = []
    for c in string.printable:
        c_list.append(c)
    print(c_list)