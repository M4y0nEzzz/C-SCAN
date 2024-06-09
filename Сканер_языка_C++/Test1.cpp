#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <functional>
#include <map>

using namespace std;

struct Person {
  string name;
  int age;
};

auto calculateAgeDifference(const Person& p1, const Person& p2) {
  return abs(p1.age - p2.age);
}

template <typename T>
T sum(T a, T b) {
  return a + b;
}

int main() {
  int arr = new int[5];

  cout << "Введите 5 чисел: ";
  for (int i = 0; i < 5; i++) {
    cin >> arr[i];
  }

  sort(arr, arr + 5);

  cout << "Отсортированный массив: ";
  for (int i = 0; i < 5; i++) {
    cout << arr[i] << " ";
  }
  cout << endl;

  delete[] arr;

  vector<int> numbers = {1, 2, 3, 4, 5};

  for (int number : numbers) {
    cout << number << " ";
  }
  cout << endl;

  if (numbers.size() > 5) {
    cout << "Вектор содержит более 5 элементов." << endl;
  } else {
    cout << "Вектор содержит 5 или менее элементов." << endl;
  }

  map<string, int> ages;
  ages["Иван"] = 30;
  ages["Мария"] = 25;

  while (ages.size() > 0) {
    cout << "Имя: " << ages.begin()->first << ", Возраст: " << ages.begin()->second << endl;
    ages.erase(ages.begin());
  }

  Person person1 = {"Иван", 30};
  Person person2 = {"Мария", 25};

  int ageDifference = calculateAgeDifference(person1, person2);

  cout << "Разница в возрасте: " << ageDifference << endl;

  const int MAX_SIZE = 10;

  static int count = 0;
  count++;

  return 0;
}