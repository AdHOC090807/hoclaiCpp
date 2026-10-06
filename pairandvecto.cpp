#include<bits/stdc++.h>
#include<iostream>
using namespace std;


int main(){
  /* pair<int,string> a;
    cin>>a.first;
    cin>>a.second;
    // pair<int,string> b = {};
    cout<<a.first <<' '<<a.second;
    */
// a.size();
   
   
 //   for(vector<int> :: iterator it = a.begin() ; it!= a.end();++it){
  //    cout<< *it << ' ';
    

  int n ;
  cin>>n;
   vector<int> a(n);
  for (int i = 0 ; i < n ; i++){
    cin>>a[i];
  }
  a.insert(a.begin()+2 , 20);
  a.erase(a.begin() + 2 , a.begin()+ 5);
  for(int x: a){
    cout<<x <<' ';
  }}