import random

# get random k elements from interator
def getSample(iterator, k):
    """
    Samples k elements from an iterable object.

    :param iterator: an object that is iterable
    :param k: the number of items to sample
    """
    # fill the reservoir to start
    result = [next(iterator) for _ in range(k)]

    n = k

    for item in iterator:
        n += 1
        s = random.randint(0, n)
        if s < k:
            result[s] = item

    return result

def getSubset(list, k):
    if k == 0:
        return []
    elif len(list) > k:
        return getSample(iter(list),k)
    else:
        return list