#ifndef BRIDGE_H
#define BRIDGE_H

#include <algorithm>
#include <array>
#include <vector>
#include <map>
#include <string>
#include <iostream>
#include <iomanip>
#include <random>
#include <tuple>
#include <functional>
#include "Results.h"


using Card = int;
typedef std::array<Card, 13> HAND;

int points();
int points(const HAND&);
int suitLength(char suit);
int suitLength(const HAND&, char suit);
extern HAND north;
extern HAND east;
extern HAND south;
extern HAND west;
extern int N;
extern std::map<int, int> partnershipPts;

#endif

