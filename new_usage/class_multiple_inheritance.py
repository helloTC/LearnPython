#!/usr/bin/env python
# coding=utf-8

# Understand Method Resolution Order (MRO) for multiple inheritance
class A:
    def test(self):
        print('A')

class C:
    def test(self):
        print('C')

class B(C):
    pass

class D(A,B):
    pass

class E(B,A):
    pass

class F(C,A):
    pass

if __name__ == '__main__':
    D().test()
    E().test()
    F().test()
