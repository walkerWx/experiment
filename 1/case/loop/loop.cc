
int evaluate(int n) {
    int y = 0;
    for (int i = 0;i < n; ++i) {
        y += i; 
    }

    for (int i = 0; i < n; ++i) {
        y -= 2*i;
    }
    return y;
}
