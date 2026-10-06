#include<bits/stdc++.h>
#include<iostream>
using namespace std;



void sang(){
    int n ;
    cin>>n;
    vector<bool> nt (n+1,true);
    nt[0] = nt[1] = false;
    for (int i = 2 ; i<= sqrt(n) ; i++){
        if (nt[i]== true ){
            for (int j = i*i ; j<= n; j+= i){
                nt[j] = false;
            }
        }
    }
    int cnt = 0;
    for (int i = 0 ; i <= n; i++){
        if (nt[i] == true){
            cnt++;
        }
    }
    cout<<cnt;
}


int main(){
    
    sang();
    


}