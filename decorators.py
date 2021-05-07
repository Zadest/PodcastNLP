# -*- coding : utf8 -*-

import time

def timer(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(func.__name__,"took",end-start,'seconds')
        return result
    return wrapper
