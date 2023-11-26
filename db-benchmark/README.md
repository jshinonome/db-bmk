## pykx vs polars

### Generate Data

Use script from ![db-benchmark](https://github.com/duckdblabs/db-benchmark) to generate data.

```bash
# creates G1_1e7_1e2_0_0.csv
Rscript _data/groupby-datagen.R 1e7 1e2 0 0
```

### Setup Python Env

```
pip install pykx polars
```

### Running Script

```
python db-benchmark/pykx-bmk.py
python db-benchmark/polars-bmk.py
```

### Benchmarks

| task                        | pykx mem(gb) | pykx time(ms) | polars mem (gb) | polars time(ms) |
| --------------------------- | -----------: | ------------: | --------------: | --------------: |
| read csv                    |        0.613 |      4612.672 |           0.649 |        1225.970 |
| sum v1 by id1               |        0.688 |        21.283 |           0.692 |          34.815 |
| sum v1 by id1:id2           |        0.986 |       100.727 |           0.736 |         118.413 |
| sum v1 mean v3 by id3       |        1.007 |        63.037 |           0.739 |         154.754 |
| mean v1:v3 by id4           |        1.007 |        60.595 |           0.743 |          41.708 |
| sum v1:v3 by id6            |        1.012 |        45.393 |           0.734 |         193.068 |
| median v3 sd v3 by id4 id5  |        1.091 |       305.644 |           0.746 |         155.055 |
| max v1 - min v2 by id3      |        1.113 |       346.257 |           0.734 |         141.168 |
| largest two v3 by id6       |        1.243 |       812.762 |           0.737 |         391.528 |
| regression v1 v2 by id2 id4 |        1.328 |      1015.523 |           0.750 |         353.580 |
| sum v3 count by id1:id6     |        3.478 |      4032.050 |           1.343 |         689.885 |
