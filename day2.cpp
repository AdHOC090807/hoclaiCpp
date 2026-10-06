#include<bits/stdc++.h>
#include<iostream>
#include<string>
using namespace std;
void swapH(int &a,int &b){
    int tmp = a;
    a = b;
    b= tmp;
}
void tanggtri(int &a){
     a += 10;
}
void sort3(int &a , int &b , int &c){
    if ( a> c){
        swap(a,c);
    }
    if ( a > b){
        swap(a,b);
    }
    if (b>c){
        swap(b,c);
    }
}
int main(){
int a = 50;
int b = 210;
int c = 3;
sort3(a,b,c);
cout <<a <<' '<<b << ' '<< c;
}