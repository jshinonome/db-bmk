import os
import timeit
from pathlib import Path

import polars as pl
import psutil


def print_usage(time: float, q: str):
    process = psutil.Process(os.getpid())
    print(
        "%-30s, mem(gb): %.3f, time(ms): %.3f"
        % (q, process.memory_info().rss / (1024**3), time * 1000)
    )


t_start = timeit.default_timer()
with pl.StringCache():
    x = pl.read_csv(
        Path.joinpath(Path.home(), "Workspace/db-benchmark/data/G1_1e7_1e2_0_0.csv"),
        dtypes={
            "id4": pl.Int32,
            "id5": pl.Int32,
            "id6": pl.Int32,
            "v1": pl.Int32,
            "v2": pl.Int32,
            "v3": pl.Float64,
        },
    ).with_columns(pl.col(["id1", "id2", "id3"]).cast(pl.Categorical))
t = timeit.default_timer() - t_start
print_usage(t, "read csv")

t_start = timeit.default_timer()
ans = x.group_by("id1").agg(pl.sum("v1").alias("v1_sum"))
t = timeit.default_timer() - t_start
print_usage(t, "sum v1 by id1")

t_start = timeit.default_timer()
ans = x.group_by(["id1", "id2"]).agg(pl.sum("v1").alias("v1_sum"))
t = timeit.default_timer() - t_start
print_usage(t, "sum v1 by id1:id2")

t_start = timeit.default_timer()
ans = x.group_by("id3").agg(
    [pl.sum("v1").alias("v1_sum"), pl.mean("v3").alias("v3_mean")]
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v1 mean v3 by id3")

t_start = timeit.default_timer()
ans = x.group_by("id4").agg(
    [
        pl.mean("v1").alias("v1_mean"),
        pl.mean("v2").alias("v2_mean"),
        pl.mean("v3").alias("v3_mean"),
    ]
)
t = timeit.default_timer() - t_start
print_usage(t, "mean v1:v3 by id4")

t_start = timeit.default_timer()
ans = x.group_by("id6").agg(
    [
        pl.sum("v1").alias("v1_sum"),
        pl.sum("v2").alias("v2_sum"),
        pl.sum("v3").alias("v3_sum"),
    ]
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v1:v3 by id6")

t_start = timeit.default_timer()
ans = x.group_by(["id4", "id5"]).agg(
    [pl.median("v3").alias("v3_median"), pl.std("v3").alias("v3_std")]
)
t = timeit.default_timer() - t_start
print_usage(t, "median v3 sd v3 by id4 id5")

t_start = timeit.default_timer()
ans = x.group_by("id3").agg([(pl.max("v1") - pl.min("v2")).alias("range_v1_v2")])
t = timeit.default_timer() - t_start
print_usage(t, "max v1 - min v2 by id3")

t_start = timeit.default_timer()
ans = (
    x.drop_nulls("v3")
    .group_by("id6")
    .agg(pl.col("v3").top_k(2).alias("largest2_v3"))
    .explode("largest2_v3")
)
t = timeit.default_timer() - t_start
print_usage(t, "largest two v3 by id6")

t_start = timeit.default_timer()
ans = x.group_by(["id2", "id4"]).agg(
    (pl.corr("v1", "v2", method="pearson") ** 2).alias("r2")
)
t = timeit.default_timer() - t_start
print_usage(t, "regression v1 v2 by id2 id4")

t_start = timeit.default_timer()
ans = x.group_by(["id1", "id2", "id3", "id4", "id5", "id6"]).agg(
    [pl.sum("v3").alias("v3"), pl.count("v1").alias("count_v1")]
)
t = timeit.default_timer() - t_start
print_usage(t, "sum v3 count by id1:id6")
