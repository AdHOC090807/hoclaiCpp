#include<bits/stdc++.h>
#include<iostream>
const double pi = 3.14;
using namespace std;
using ll  = long long ;
bool checkFibo(ll n){
    ll  fibo[100];
    fibo[0] = 0;
    fibo[1] = 1;
    for (int i = 2 ; i <=92 ; i++){
        fibo[i] = fibo[i-1] +fibo[i-2];

    }
    for (int i = 0 ; i<=92;i++){
        if (fibo[i]==n) return true;
    }
    return false;


}

int main (){
    ll n;
    cin>>n;
    checkFibo(n) == false ? cout<<0 : cout<<1;
    return 0;
}