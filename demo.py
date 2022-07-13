import multiprocessing as mp
import time
import random


def worker(number):
    time.sleep(0.5 * random.random())
    return number, time.time()


def collect_result(result):
    # do some processing on the result and return the desired data
    return result


def try_apply(pool: mp.Pool, data):
    ts = time.time()
    res = [pool.apply(worker, (num,)) for num in data]
    for num, te in res:
        print(f"{num} -> {te - ts}")


def try_apply_async(pool: mp.Pool, data):
    ts = time.time()
    results = [pool.apply_async(worker, (num,), callback=collect_result) for num in data]
    for res in results:
        num, te = res.get()
        print(f"{num} -> {te - ts}")


def try_map(pool: mp.Pool, data):
    ts = time.time()
    results = pool.map(worker, data, chunksize=2)
    for res in results:
        print(f"{res[0]} -> {res[1] - ts}")


def try_map_async(pool: mp.Pool, data):
    ts = time.time()
    results = pool.map_async(worker, data, chunksize=2)
    for res in results.get():
        print(f"{res[0]} -> {res[1] - ts}")


def try_imap(pool: mp.Pool, data):
    ts = time.time()
    for res in pool.imap(worker, data, chunksize=2):
        print(f"{res[0]} -> {res[1] - ts}")


def try_imap_unordered(pool: mp.Pool, data):
    ts = time.time()
    for res in pool.imap_unordered(worker, data, chunksize=2):
        print(f"{res[0]} -> {res[1] - ts}")


def invoke_multiprocess_funcs():
    data = range(9)
    pool = mp.Pool(4)

    func_list = [try_apply, try_apply_async, try_map, try_map_async, try_imap, try_imap_unordered]

    for func in func_list:
        print(f'\n {func.__name__.replace("try_", "")}()')
        func(pool, data)

    pool.close()


if __name__ == '__main__':
    invoke_multiprocess_funcs()
