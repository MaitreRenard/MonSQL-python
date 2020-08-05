#!/usr/bin/env python3
#coding: utf-8

import mysql.connector

class MonSQL(object):
    def __getattribute__(self,name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def tmp_func(*args, **kwargs):
                print(attr.__name__)
                result = attr(*args, **kwargs)
                return result
            return newfunc
        else:
            return attr
