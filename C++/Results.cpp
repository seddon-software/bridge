#include "Bridge.h"
#include "Results.h"

using namespace std;


void Results::check()
{
	if(f()) count++;
}

void Results::print() const
{
    cout << name << ": " << count * 100.0 / N << "%" << endl;
}

void Results::show() const
{
    cout << name << ": " << count << endl;
}
