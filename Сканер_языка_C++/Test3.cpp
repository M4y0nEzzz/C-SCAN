#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main()
{
    int n;
    cin >> n;
    vector<vector<int> > gr(n, vector<int>(n, 0));
    for(int i = 0; i < n; ++i){
        for(int j = 0; j < n; ++j){
            cin >> gr[i][j];
        }
    }
    for(int k = 0; k < n; ++k){
        for(int i = 0; i < n; ++i){
            for(int j = 0; j < n; ++j){
                if(gr[i][j] > gr[i][k] + gr[k][j]){
                    gr[i][j] = gr[i][k] + gr[k][j];
                }
            }
        }
    }
    for(int i = 0; i < n; ++i){
        if(gr[i][i] < 0){
            cout << "YES";
            return 0;
        }
    }
    cout << "NO";
    return 0;
}