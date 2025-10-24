#include <bits/stdc++.h>
using namespace std;
struct Student{int id; string name;};
class CircularQueue{vector<Student>buf;int head,tail,cap,count;
public:CircularQueue(int c):buf(c),head(0),tail(0),cap(c),count(0){}
bool enqueue(const Student&s){if(count==cap)return false;buf[tail]=s;tail=(tail+1)%cap;count++;return true;}
bool dequeue(Student &s){if(!count)return false;s=buf[head];head=(head+1)%cap;count--;return true;}
void printQueue()const{cout<<"Queue:\n";int idx=head;for(int i=0;i<count;i++){cout<<"  "<<buf[idx].id<<"-"<<buf[idx].name<<"\n";idx=(idx+1)%cap;}if(!count)cout<<"  [empty]\n";}};
int main(){CircularQueue q(3);q.enqueue({1,"Alice"});q.enqueue({2,"Bob"});q.enqueue({3,"Clara"});q.printQueue();Student s;q.dequeue(s);q.enqueue({4,"David"});q.printQueue();}