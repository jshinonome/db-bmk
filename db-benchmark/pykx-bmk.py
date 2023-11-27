import os
import timeit
from pathlib import Path

import psutil

import pykx as kx


def print_usage(time: float, q: str):
    process = psutil.Process(os.getpid())
    print(
        "%-30s, mem(gb): %.3f, time(ms): %.3f"
        % (q, process.memory_info().rss / (1024**3), time * 1000)
    )


t_start = timeit.default_timer()
x = kx.q.read.csv(
    path=Path.joinpath(Path.home(), "Workspace/db-benchmark/data/G1_1e7_1e2_0_0.csv"),
    types="SSSIIIIIF",
    as_table=True,
)
t = timeit.default_timer() - t_start
print_usage(t, "read csv")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "v1_sum": "sum v1",
    },
    by={"id1": "id1"},
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v1 by id1")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "v1_sum": "sum v1",
    },
    by={"id1": "id1", "id2": "id2"},
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v1 by id1:id2")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "v1_sum": "sum v1",
        "v3_mean": "avg v3",
    },
    by={"id3": "id3"},
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v1 mean v3 by id3")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "v1_mean": "avg v1",
        "v2_mean": "avg v2",
        "v3_mean": "avg v3",
    },
    by={"id4": "id4"},
)
t = timeit.default_timer() - t_start
print_usage(t, "mean v1:v3 by id4")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "v1_sum": "sum v1",
        "v2_sum": "sum v2",
        "v3_sum": "sum v3",
    },
    by={"id6": "id6"},
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v1:v3 by id6")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "v3_median": "med v3",
        "v3_std": "dev v3",
    },
    by={
        "id4": "id4",
        "id5": "id5",
    },
)
t = timeit.default_timer() - t_start
print_usage(t, "median v3 sd v3 by id4 id5")

t_start = timeit.default_timer()
ans = kx.q.qsql.select(
    x,
    {
        "range_v1_v2": "max[v1] - min v2",
    },
    by={
        "id3": "id3",
    },
)
t = timeit.default_timer() - t_start
print_usage(t, "max v1 - min v2 by id3")

t_start = timeit.default_timer()

ans = kx.q.qsql.select(
    x,
    {
        "largest2_v3": "{m: max x; $[1<sum x = m;2#m;m, max x except m]} v3",
    },
    by={
        "id6": "id6",
    },
    where=["not null v3"],
)
ans = ans.ungroup()
# ans = kx.q.qsql.select(
#     x,
#     {
#         "id6": "id6",
#         "largest2_v3": "v3",
#     },
#     where=["not null v3", "v3 >= ({(asc x)@1};v3) fby id6"],
# )
t = timeit.default_timer() - t_start
print_usage(t, "largest two v3 by id6")

ans = kx.q.qsql.select(
    x,
    {
        "r2": "(v1 cor v2) xexp 2",
    },
    by={
        "id2": "id2",
        "id4": "id4",
    },
)
t = timeit.default_timer() - t_start
print_usage(t, "regression v1 v2 by id2 id4")

ans = kx.q.qsql.select(
    x,
    {
        "v3": "sum v3",
        "count_v1": "count v1",
    },
    by={
        "id1": "id1",
        "id2": "id2",
        "id3": "id3",
        "id4": "id4",
        "id5": "id5",
        "id6": "id6",
    },
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v3 count by id1:id6")
