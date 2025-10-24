#include <iostream>
#include <string>
#include <map> // use map instead of unordered_map for old compilers

using namespace std;

struct Book
{
    string isbn;
    string title;
    int copies;
};

class Library
{
private:
    map<string, Book> m; // replaced unordered_map with map for compatibility

public:
    void add(Book b)
    {
        m[b.isbn] = b;
    }

    bool borrow(string i)
    {
        if (m.find(i) == m.end() || m[i].copies <= 0)
            return false;
        m[i].copies--;
        return true;
    }

    bool ret(string i)
    {
        if (m.find(i) == m.end())
            return false;
        m[i].copies++;
        return true;
    }

    void show()
    {
        for (map<string, Book>::iterator it = m.begin(); it != m.end(); ++it)
        {
            cout << it->second.isbn << " " << it->second.title
                 << " copies:" << it->second.copies << "\n";
        }
    }
};

int main()
{
    Library l;

    Book b1;
    b1.isbn = "1";
    b1.title = "C++";
    b1.copies = 2;
    l.add(b1);

    Book b2;
    b2.isbn = "2";
    b2.title = "DSA";
    b2.copies = 1;
    l.add(b2);

    l.show();
    l.borrow("1");
    l.show();
    l.ret("1");
    l.show();

    return 0;
}
