#include<bits/stdc++.h>
#include<iostream>
using namespace std;

bool ktra(int a){
    for (int i = 2; i*i <= a; i++){
        if(a%i == 0 )return false;
    }
    return a > 1;
}

double tbcongngto(int a[] ,int n ){
    double sum = 0;
    double dem = 0;
    for (int i = 0 ; i < n ; i++){
        if (ktra(a[i]) == true){
            dem++;
            sum+= a[i];
        }
    }
    if (dem != 0){
    double tb = sum / dem;
return tb;}
    else{ return 0;}
    
}


int main(){
    int n ;
    cin>>n;
    int a[n];
    for (int &x : a){
        cin>>x;
    }
    cout<<tbcongngto(a,n);
}