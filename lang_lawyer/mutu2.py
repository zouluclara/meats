
def dep2(n):
    from circ1 import dep1
    if n > 0:
        print n,
        dep1(n-1)

if __name__=='__main__':
    dep2(int(raw_input()))

