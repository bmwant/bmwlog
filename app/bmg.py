# -*- coding: utf-8 -*-
"""
Bottle generator for forms and templates based on models
"""
__author__ = 'Most Wanted'


import sys
import inspect
import peewee

current_module = sys.modules[__name__]


def print_classes():
    from app import models
    for name, obj in inspect.getmembers(models, inspect.isclass):
        if obj.__module__ == models.__name__:
            print(obj)
            for field_name, field in vars(obj).iteritems():
                #print()
                if isinstance(field, peewee.FieldDescriptor):
                    print(field_name)
            break

#clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)

if __name__ == '__main__':
    print_classes()