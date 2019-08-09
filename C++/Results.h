#ifndef RESULTS_H
#define RESULTS_H

#include <string>
#include <functional>

typedef bool (*FP)();

class Results
{
public:
	Results(const std::string& name, std::function<bool()> f) : name(name), f(f), count(0) {}
	void check();
    void show() const;
    void print() const;
private:
	std::string name;
//	FP fp;
	std::function<bool()> f;
	int count;
};


#endif
