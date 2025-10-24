#include <bits/stdc++.h>
using namespace std;
struct Fee
{
	int id;
	int sid;
	double amt;
};
struct Node
{
	Fee f;
	Node*l, *r;
	int h;
	Node(Fee x): f(x), l(0), r(0), h(1) {}
};
int h(Node*n)
{
	return n ? n->h : 0;
}
int bf(Node*n)
{
	return n ? h(n->l) - h(n->r) : 0;
}
void upd(Node*n)
{
	if(n)n->h = 1 + max(h(n->l), h(n->r));
}
Node*rotR(Node*y)
{
	Node*x = y->l;
	Node*t = x->r;
	x->r = y;
	y->l = t;
	upd(y);
	upd(x);
	return x;
}
Node*rotL(Node*x)
{
	Node*y = x->r;
	Node*t = y->l;
	y->l = x;
	x->r = t;
	upd(x);
	upd(y);
	return y;
}
Node*ins(Node*r, Fee f)
{
	if(!r)return new Node(f);
	if(f.id < r->f.id)r->l = ins(r->l, f);
	else if(f.id > r->f.id)r->r = ins(r->r, f);
	else return r;
	upd(r);
	int b = bf(r);
	if(b > 1 && f.id < r->l->f.id)return rotR(r);
	if(b < -1 && f.id > r->r->f.id)return rotL(r);
	if(b > 1 && f.id > r->l->f.id)
	{
		r->l = rotL(r->l);
		return rotR(r);
	}
	if(b < -1 && f.id < r->r->f.id)
	{
		r->r = rotR(r->r);
		return rotL(r);
	}
	return r;
}
void inorder(Node*r)
{
	if(!r)return;
	inorder(r->l);
	cout << r->f.id << " " << r->f.sid << " " << r->f.amt << "\n";
	inorder(r->r);
}
int main()
{
	Node*r = 0;
	r = ins(r, {1, 101, 500});
	r = ins(r, {2, 102, 250});
	r = ins(r, {3, 103, 400});
	inorder(r);
}
