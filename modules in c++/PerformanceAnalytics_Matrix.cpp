#include <iostream>
#include <vector>
#include <string>
#include <numeric> // for accumulate

using namespace std;

int main()
{
    // Initialize matrix manually (no brace-initialization)
    vector<vector<double> > m(3, vector<double>(3, 0.0));
    m[0][0] = 78; m[0][1] = 85; m[0][2] = 90;
    m[1][0] = 88; m[1][1] = 76; m[1][2] = 80;
    m[2][0] = 92; m[2][1] = 89; m[2][2] = 94;

    vector<int> id(3);
    id[0] = 101; id[1] = 102; id[2] = 103;

    vector<string> sub(3);
    sub[0] = "Math"; sub[1] = "CS"; sub[2] = "Phys";

    cout << "Performance:\n";
    for (int i = 0; i < 3; i++)
    {
        double sum = accumulate(m[i].begin(), m[i].end(), 0.0);
        double avg = sum / m[i].size();
        cout << "Student " << id[i] << " avg: " << avg << "\n";
    }

    return 0;
}
