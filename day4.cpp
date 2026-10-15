#include<bits/stdc++.h>
#include <iostream>
using namespace std;


class Employee {
private:
    string name;
    double salary = 0;

public:
    void setInfo(string name, double salary) {
        this->name = name ;
        this-> salary = salary;
    }

    void display() ;
};
void Employee::display(){
    
        cout << name << ' ' << salary << '\n';
    
}
int main(){
    Employee s1;
    string name ; double salary;
    getline(cin,name);
    cin>>salary;
    s1.setInfo(name,salary);
    s1.display();
    
    
}