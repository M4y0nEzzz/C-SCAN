#include <iostream>
#include <set>
using namespace std;

const long long Inf = 1e18;

int main() {
    // fast input-output
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    set<long long> s;
    multiset<long long> r;
    s.insert(-Inf);
    s.insert(Inf);
    r.insert(2 * Inf);

    int n;
    for(cin >> n; n > 0; --n) {
       string cmd;
       cin >> cmd;
       if (cmd == L"ADD") {
          int x;
          cin >> x;
          auto it = s.find(x);
          if (it == s.end()) {
             auto right = s.upper_bound(x);
             auto left = right;
             --left;

             r.erase(r.find(*right - *left));
             r.insert(x - *left);
             r.insert(*right - x);
             s.insert(x);
          }
       } else if (cmd == L"DEL") {
           int x;
           cin >> x;
           auto it = s.find(x);
           if (it != s.end()) {
             auto right = s.upper_bound(x);
             auto left = right;
            --left;
            --left;
            r.erase(r.find(x-*left));
             r.erase(r.find(*right - x));
             r.insert(*right - *left);
             s.erase(x);

       } }else {
           cout<<*r.begin()<<endl;
       }

    }
}

