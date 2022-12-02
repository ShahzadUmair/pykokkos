#!/bin/bash


# fn_2d_list = [
#   ["var", 0],
#   ["mean", 0],
#   ["sum", 0],
#   ["transpose"],
#   ["divide", 10],
#   ["power", 2],
# ]

# fn_1d_list = [
#     ["log"],
#     ["exp"],
#     ["logical_not"],
#     ["all"],
#     ["multiply", 2]
# ]

# fn_2arr_list = [
#     ["add"],
# ]

# fn_2arr_1d_1d_list = [
#     ["index"],
#     ["in1d"],
# ]

# "zeros"

export NUMEXPR_MAX_THREADS=12
# python3 /pykokkos/profiling/res.py var 0
# python3 /pykokkos/profiling/res.py mean 0
#  python3 /pykokkos/profiling/res.py sum 0
# python3 /pykokkos/profiling/res.py transpose
# python3 /pykokkos/profiling/res.py divide 10
# python3 /pykokkos/profiling/res.py power 2

# python3 /pykokkos/profiling/res.py log
# python3 /pykokkos/profiling/res.py exp
# python3 /pykokkos/profiling/res.py logical_not
# python3 /pykokkos/profiling/res.py all
# python3 /pykokkos/profiling/res.py multiply 2

# python3 /pykokkos/profiling/res.py add

# python3 /pykokkos/profiling/res.py index
python3 /pykokkos/profiling/res.py in1d

# python3 /pykokkos/profiling/res.py zeros