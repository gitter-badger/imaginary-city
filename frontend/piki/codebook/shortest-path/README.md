# Floyd-Warshall Algorithm

```python
# w = n*n array 

d = [[w[i][j] for j in range(n)] for i in range(n)]

for i in range(n):
    d[i][i] = 0

for k in range(n):
    for i in range(n):
        for j in range(n):
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])
```
