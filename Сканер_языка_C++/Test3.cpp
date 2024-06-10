#include <iostream>

using namespace std;

int main() { //comment
    double number = 0.0e+1;
    /*
    comment
    comment
    comment
    */

    if (number > 5) {
        cout << text << endl;
    } else {
        cout << "Number is less than or equal to 5" << endl;
    }

    for (int i = 0; i < number; i++) {
        cout << i << " ";
    }

    while (number > 0) {
        number--;
    }

    switch (number) {
        case 0:
            cout << "nNumber is now 0" << endl;
            break;
        default:
            cout << "nNumber is not 0" << endl;
    }

    int numbers[] = {1, 2, 3, 4, 5};
    for (int num : numbers) {
        cout << num << " ";
    }

    int a;
    cin >> a;
    cout << a;
    cout << endl;

    return 0;
}