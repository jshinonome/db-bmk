## pykx vs polars

### Generate Data

Use script from [db-benchmark](https://github.com/duckdblabs/db-benchmark) to generate data.

```bash
# creates G1_1e7_1e2_0_0.csv
Rscript _data/groupby-datagen.R 1e7 1e2 0 0
```

### Setup Python Env

```
pip install pykx polars
```

### Running Script

Polars queries are from [polars-groupby](https://github.com/duckdblabs/db-benchmark/blob/master/polars/groupby-polars.py)

```bash
python db-benchmark/pykx-bmk.py
python db-benchmark/polars-bmk.py
```

### Benchmarks

mem(gb): memory, the lower the better. time(ms): time used, the lower the better

| task                        | pykx mem(gb) | pykx time(ms) | polars mem (gb) | polars time(ms) | speed vs pykx |
| --------------------------- | -----------: | ------------: | --------------: | --------------: | ------------: |
| read csv                    |        0.612 |      3750.128 |           0.649 |        1292.889 |        2.900x |
| sum v1 by id1               |        0.687 |        19.143 |           0.713 |          44.714 |        0.428x |
| sum v1 by id1:id2           |        0.986 |        89.125 |           0.744 |         104.961 |        0.849x |
| sum v1 mean v3 by id3       |        1.006 |        68.805 |           0.751 |         134.462 |        0.511x |
| mean v1:v3 by id4           |        1.006 |        52.704 |           0.755 |          36.087 |        1.460x |
| sum v1:v3 by id6            |        1.012 |        40.708 |           0.749 |         164.079 |        0.248x |
| median v3 sd v3 by id4 id5  |        1.090 |       295.424 |           0.757 |         130.586 |        2.262x |
| max v1 - min v2 by id3      |        1.113 |       301.650 |           0.744 |         144.374 |        2.089x |
| largest two v3 by id6       |        1.243 |       492.052 |           0.746 |         352.535 |        1.395x |
| regression v1 v2 by id2 id4 |        1.328 |       178.138 |           0.751 |         325.847 |        0.546x |
| sum v3 count by id1:id6     |        3.478 |      2604.182 |           1.355 |         617.948 |        4.214x |
