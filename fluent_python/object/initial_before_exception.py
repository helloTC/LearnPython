#!/usr/bin/env python
# coding=utf-8

class Gizmo(object):
    def __init__(self):
        print("ID:{0}".format(id(self)))

if __name__ == "__main__":
    giz = Gizmo()
    giz_error = Gizmo()*10
