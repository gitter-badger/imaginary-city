# 並查集

```
struct DisjoinSet{
    vector<int> fat;
    DisjoinSet(int n){
        fat = vector<int>(n, 0);
        for(int lx = 0;lx < n;lx++)
            fat[lx] = lx;
    }
 
    int root(int a){
        if(fat[a] == a) return a;
        fat[a] = root(fat[a]);
        return fat[a];
    }
 
    void join(int a, int b){
        fat[root(a)] = root(b);
        return;
    }
};
```
