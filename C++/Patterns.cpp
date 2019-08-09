#include "Bridge.h"
#include "Patterns.h"

using namespace std;

bool eastBidsWeakTwoInHearts()
{
    return
        suitLength(east, 'h') >= 6 &&
        points(east) >= 5 && points(east) <= 9;
}

bool eastWestFit6()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    return
        eastBidsWeakTwoInHearts() && fit == 6;
}

bool eastWestFit7()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    return
        eastBidsWeakTwoInHearts() && fit == 7;
}

bool eastWestFit8()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    return
        eastBidsWeakTwoInHearts() && fit == 8;
}

bool eastWestFit9()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    return
        eastBidsWeakTwoInHearts() && fit == 9;
}

bool eastWestFit10()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    return
        eastBidsWeakTwoInHearts() && fit == 10;
}

bool eastWestFit11()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    return
        eastBidsWeakTwoInHearts() && fit == 11;
}

bool eastsWeakTwoGoesDownAndWeHaveSevenCardFit()
{
    return eastsWeakTwoGoesDownAndWeHaveNCardFit(7);
}

bool eastsWeakTwoGoesDownAndWeHaveEightCardFit()
{
    return eastsWeakTwoGoesDownAndWeHaveNCardFit(8);
}

bool eastsWeakTwoGoesDownAndWeHaveNineCardFit()
{
    return eastsWeakTwoGoesDownAndWeHaveNCardFit(9);
}

bool eastsWeakTwoGoesDownAndWeHaveTenCardFit()
{
    return eastsWeakTwoGoesDownAndWeHaveNCardFit(10);
}

bool eastsWeakTwoGoesDownAndWeHaveNCardFit(int n)
{
    return
        (
//            suitLength(south, 'c') + suitLength(north, 'c') == n ||
//            suitLength(south, 'd') + suitLength(north, 'd') == n ||
            suitLength(south, 's') + suitLength(north, 's') == n
        ) && (
            eastsWeakTwoGoesDown6() ||
            eastsWeakTwoGoesDown7() ||
            eastsWeakTwoGoesDown8() ||
            eastsWeakTwoGoesDown9()
        );
}

bool eastsWeakTwoGoesDown6()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    int pts = points(west) + points(east);
    return eastBidsWeakTwoInHearts() && fit == 6;
}

bool eastsWeakTwoGoesDown7()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    int pts = points(west) + points(east);
    return eastBidsWeakTwoInHearts() && fit == 7 && pts < 23;
}

bool eastsWeakTwoGoesDown8()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    int pts = points(west) + points(east);
    return eastBidsWeakTwoInHearts() && fit == 8 && pts < 20;
}

bool eastsWeakTwoGoesDown9()
{
    int fit = suitLength(west, 'h') + suitLength(east, 'h');
    int pts = points(west) + points(east);
    return eastBidsWeakTwoInHearts() && fit == 9 && pts < 17;
}




