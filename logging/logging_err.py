import functools


def exception(logger):

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
                raise
        return wrapper
    return decorator