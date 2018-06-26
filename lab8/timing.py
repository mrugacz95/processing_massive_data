import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms result is %d' % (f.__name__, (time2 - time1) * 1000.0, ret))
        return ret

    return wrap