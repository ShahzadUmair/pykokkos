import sys
import pykokkos as pk
import numpy as np
import pandas as pd
from time import perf_counter
from statistics import mean, median
from math import log10, floor
import gc


fn_2d_list = [
  "var",
  "mean",
  "sum",
  "transpose",
  "divide",
  "power",
  "log",
]

fn_1d_list = [
    # "log",
    "exp",
    "logical_not",
    "all",
    "multiply",
]

fn_2arr_list = [
    "add",
]

fn_2arr_1d_1d_list = [
    "index",
    "in1d",
]

fn_2arr_1d_1d_types_list = [
    [pk.double, pk.int32],
    [pk.double, pk.double],
]

mem = [10, 100, 1000, 10000, 100000, 1000000]

def round2_ms(x):
    x *= 1000
    return round(x, -int(floor(log10(abs(x)))) + 1)


def pk_2arr_1d_1d_res(fn):
    print(fn, "pk2arr_1d_1d_res")
    res = ["pk"]
    mems_to_test = mem if fn[0] != "in1d" else [i//10 for i in mem]

    for k in range(len(mems_to_test)):
        s = mem[k]
        arr = [i for i in range(s)]
        np_arr = np.asarray(arr, dtype=np.double)

        pk_arrA = pk.View([s], fn_2arr_1d_1d_types_list[fn_2arr_1d_1d_list.index(fn[0])][0])
        pk_arrA[:] = np_arr
        
        arr = [i for i in range(s)]
        np_arr = np.asarray(arr, dtype=np.double)
        pk_arrB = pk.View([s], fn_2arr_1d_1d_types_list[fn_2arr_1d_1d_list.index(fn[0])][1])
        pk_arrB[:] = np_arr

        pk_fn = getattr(pk, fn[0])
        
        times = []
        for _ in range(1):
            start = perf_counter()
            pk_fn(pk_arrA, pk_arrB)
            end = perf_counter()
            times.append(end-start)
        
        res.append(round2_ms(mean(times)))
        res.append(round2_ms(median(times)))

    return res

def np_2arr_1d_1d_res(fn):
    res = ["np"]
    for s in mem:
        arr = [i for i in range(s)]
        np_arrA = np.asarray(arr)

        arr = [i for i in range(s)]
        np_arrB = np.asarray(arr)

        np_fn = None
        if (fn[0] != "index"):
            np_fn = getattr(np, fn[0])
        
        times = []
        
        for i in range(50):
            start = perf_counter()
            if np_fn != None:
                np_fn(np_arrA, np_arrB)
            else:
                np_arrA[np_arrB]
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def pk_2arr_2d_1d_res(fn):
    print(fn, "pk_2arr_2d_1d_res")
    res = ["pk"]
    for s in mem:
        arr = [[i for i in range(10)] for i in range(s)]
        np_arr = np.asarray(arr, dtype=np.double)

        pk_arrA = pk.View([s, 10], pk.double)
        pk_arrA[:] = np_arr
        
        arr = [i for i in range(10)]
        np_arr = np.asarray(arr, dtype=np.double)
        pk_arrB = pk.View([10], pk.double)
        pk_arrB[:] = np_arr

        pk_fn = getattr(pk, fn[0])
        
        times = []
        for i in range(50):
            start = perf_counter()
            pk_fn(pk_arrA, pk_arrB)
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def np_2arr_2d_1d_res(fn):
    res = ["np"]
    for s in mem:
        arr = [[i for i in range(10)] for i in range(s)]
        np_arrA = np.asarray(arr)

        arr = [i for i in range(10)]
        np_arrB = np.asarray(arr)

        np_fn = None
        if (fn[0] != "index"):
            np_fn = getattr(np, fn[0])
        
        times = []
        
        for i in range(50):
            start = perf_counter()
            if np_fn != None:
                np_fn(np_arrA, np_arrB)
            else:
                np_arrA[np_arrB]
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def pk_2d_res(fn):
    print(fn, "pk_2d_res")
    res = ["pk"]
    for s in mem:
        arr = [[j for j in range(10)] for i in range(s)]
        np_arr = np.asarray(arr, dtype=np.double)
        pk_arr = pk.View([s, 10], pk.double)
        pk_arr[:] = np_arr

        pk_fn = getattr(pk, fn[0])

        times = []
        for i in range(50):
            start = perf_counter()
            if (len(fn) == 2):
                pk_fn(pk_arr, fn[1])
            else:
                pk_fn(pk_arr)
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res



def np_2d_res(fn):
    res = ["np"]
    for s in mem:
        arr = [[j for j in range(10)] for i in range(s)]
        np_arr = np.asarray(arr)

        np_fn = getattr(np, fn[0])
        
        times = []

        for _ in range(50):
            start = perf_counter()
            if (len(fn) == 2):
                np_fn(np_arr, fn[1])
            else:
                np_fn(np_arr)
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def pk_res(fn):
    print(fn, "pk_res")
    res = ["pk"]
    for s in mem:
        arr = [i for i in range(1, s+1)]
        np_arr = np.asarray(arr, dtype=np.double)
        pk_arr = pk.View([s], pk.double)
        pk_arr[:] = np_arr

        pk_fn = getattr(pk, fn[0])
        
        times = []
        for _ in range(50):
            start = perf_counter()
            if (len(fn) == 2):
                pk_fn(pk_arr, fn[1])
            else:
                pk_fn(pk_arr)
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def np_res(fn):
    res = ["np"]
    for s in mem:
        arr = [i for i in range(1,s+1)]
        np_arr = np.asarray(arr)

        np_fn = getattr(np, fn[0])
        
        times = []
        
        for i in range(50):
            start = perf_counter()
            if (len(fn) == 2):
                np_fn(np_arr, fn[1])
            else:
                np_fn(np_arr)
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def test_zeros_pk():
    print("Zeros")
    res = ["pk"]
    for s in mem:
        times = []
        for i in range(50):
            start = perf_counter()
            pk.zeros([s, 10])
            end = perf_counter()
            times.append(end-start)
    
        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res

def test_zeros_np():
    res = ["np"]
    for s in mem:
        times = []
        for i in range(50):
            start = perf_counter()
            np.zeros([s, 10])
            end = perf_counter()
            times.append(end-start)

        res.append(round2_ms(mean(times[10:])))
        res.append(round2_ms(median(times)))
    return res


def main():
    # pk.set_default_space(pk.ExecutionSpace.Serial)

    args = sys.argv[1:]

    fn = args[0]
    fn_in = int(args[1]) if len(args) > 1 else None

    sig = [fn , fn_in] if fn_in is not None else [fn]

    io_file = "/pykokkos/profiling/team1.csv"
    
    try:
        df = pd.read_csv(io_file, header=0, index_col=[0])
    except Exception as e:
        cols = []
        for m in mem:
            cols.extend([str(m) + " (mean)", str(m) + " (med)"])
        df = pd.DataFrame(columns=["fn" , *cols])

    if not df.loc[df['fn'] == fn].empty:
        return
    
    pk_fn = np_fn = None
    pk_args = np_args = [sig]

    if fn in fn_2d_list:
        pk_fn = pk_2d_res
        np_fn = np_2d_res

    if fn in fn_1d_list:
        pk_fn = pk_res
        np_fn = np_res
    
    if fn in fn_2arr_list:
        pk_fn = pk_2arr_2d_1d_res
        np_fn = np_2arr_2d_1d_res
    
    if fn in fn_2arr_1d_1d_list:
        pk_fn = pk_2arr_1d_1d_res
        np_fn = np_2arr_1d_1d_res
    
    if fn == "zeros":
        pk_fn = test_zeros_pk
        np_fn = test_zeros_np
        pk_args = np_args = []

    fn_row = [fn] + [""] * (len(df.columns) - 1)
    df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = fn_row
    
    
    np_row = np_fn(*np_args)
    df.loc[df.index.max() + 1] = np_row

    pk_row = pk_fn(*pk_args)
    df.loc[df.index.max() + 1] = pk_row

    # df.to_csv(io_file)
    print(df)

if __name__ == "__main__":
    main()