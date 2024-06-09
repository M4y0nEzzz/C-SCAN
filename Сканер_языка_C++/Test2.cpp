#include <iostream>
#include <vector>

using namespace std;

int main()
{
    int n;
    cin >> n;
    vector<int> v(n);

    for(int count = 0; count < v.size(); count++)
    {
        v[count] = count + 1;
    }
}