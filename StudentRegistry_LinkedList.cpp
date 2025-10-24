// StudentRegistry_LinkedList.cpp
#include <bits/stdc++.h>
using namespace std;

struct Student
{
    int id;
    string name;
    int year;
};
struct Node
{
    Student data;
    Node* next;
    Node(const Student& s): data(s), next(NULL) {}
};

class StudentRegistry
{
private:
    Node* head;
public:
    StudentRegistry(): head(NULL) {}
    ~StudentRegistry()
    {
        Node* cur = head;
        while(cur)
        {
            Node* tmp = cur;
            cur = cur->next;
            delete tmp;
        }
    }
    void addStudent(const Student& s)
    {
        Node* node = new Node(s);
        node->next = head;
        head = node;
    }
    bool removeStudent(int id)
    {
        Node* cur = head;
        Node* prev = NULL;
        while(cur)
        {
            if(cur->data.id == id)
            {
                if(prev) prev->next = cur->next;
                else head = cur->next;
                delete cur;
                return true;
            }
            prev = cur;
            cur = cur->next;
        }
        return false;
    }
    Student* findStudent(int id)
    {
        Node* cur = head;
        while(cur)
        {
            if(cur->data.id == id) return &cur->data;
            cur = cur->next;
        }
        return NULL;
    }
    void printAll() const
    {
        Node* cur = head;
        cout << "Student Registry:\n";
        if(!cur) cout << "  [empty]\n";
        while(cur)
        {
            cout << "  ID: " << cur->data.id << " | Name: " << cur->data.name << " | Year: " << cur->data.year << '\n';
            cur = cur->next;
        }
    }
};

int main()
{
    StudentRegistry reg;

    Student s1;
    s1.id = 101; s1.name = "Alice"; s1.year = 2;
    reg.addStudent(s1);

    Student s2;
    s2.id = 102; s2.name = "Bob"; s2.year = 3;
    reg.addStudent(s2);

    Student s3;
    s3.id = 103; s3.name = "Clara"; s3.year = 1;
    reg.addStudent(s3);

    reg.printAll();

    cout << "\nFind ID 102:\n";
    Student* found = reg.findStudent(102);
    if(found) cout << "  Found: " << found->name << "\n";
    else cout << "  Not found\n";

    reg.removeStudent(102);

    cout << "\nAfter removal:\n";
    reg.printAll();
    return 0;
}
