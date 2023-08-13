class DSU {
    constructor(n) {
        this.n = n;
        this.parent = {};
        this.rank = {};
        for (let i = 1; i <= n; i++) {
            this.makeSet(i);
        }
    }

    makeSet(v) {
        this.parent[v] = v;
        this.rank[v] = 0;
    }

    findSet(v) {
        if (v === this.parent[v]) {
            return v;
        }
        this.parent[v] = this.findSet(this.parent[v])
        return this.parent[v];
    }

    unionSets(a, b) {
        a = this.findSet(a);
        b = this.findSet(b);

        if (a !== b) {
            if (this.rank[a] < this.rank[b]) {
                const c = a;
                a = b;
                b = c;
            }
            this.parent[b] = a;
            if (this.rank[a] === this.rank[b]) {
                this.rank[a]++;
            }
        }
    }

    * getSet (v) {
        const u = this.findSet(v);
        for (let i = 1; i <= this.n; i++) {
            if (this.findSet(i) === u) {
                yield i;
            }
        }
    }
}
