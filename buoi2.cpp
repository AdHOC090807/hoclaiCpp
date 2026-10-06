#include<bits/stdc++.h>
#include<iostream>
#include<string>
const double pi = 3.14;
using namespace std;

   /*  int a[10];
   
    for (int &x : a){
        cin>>x;
    }
    int S = 0;
    for (int x : a){
        S+=x;
    }
    int Schan = 0;
    for (int x : a){
        if (x%2 == 0){
            Schan+= x;
        }
    }
    cout<<"Tong chuoi : "<<S<<'\n';
    cout<<"Tong chan : "<<Schan;
}*/ 

int main(){
   // string nhé .
   int age;
   cin>>age;
   cin.ignore(1000, '\n');
   string name ;
   getline(cin,name);
   cout<< "Toi nam nay "<< age << ' ' << "ten la "<< name;


}