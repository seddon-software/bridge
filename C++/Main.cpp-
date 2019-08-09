#include "Header.h"

using namespace std;


bool eastBidsWeakTwoInHearts(int = 0)
{
    return
        suitLength(east, 'h') >= 6 &&
        points(east) >= 5 && points(east) <= 9;
}

bool northSouthPointsAfterWeakTwoHearts(int p)
{
    int pts   = points(north) + points(south);
    return eastBidsWeakTwoInHearts() && pts == p;
}

bool northSouthFitAfterWeakTwoHearts(int _fit)
{
    int spadesFit   = suitLength(north, 's') + suitLength(south, 's');
    int heartsFit   = suitLength(north, 'h') + suitLength(south, 'h');
    int diamondsFit = suitLength(north, 'd') + suitLength(south, 'd');
    int clubsFit    = suitLength(north, 'c') + suitLength(south, 'c');
    int fit = max(spadesFit, heartsFit);
    fit = max(fit, diamondsFit);
    fit = max(fit, clubsFit);
    return eastBidsWeakTwoInHearts() && fit == _fit;
}

bool northSouthCanMakeFourSpadesAfterWeakTwoHearts(int fit)
{
    int pts = points(north) + points(south);
    int spadesFit   = suitLength(north, 's') + suitLength(south, 's');
    
    return
        eastBidsWeakTwoInHearts() && spadesFit == fit &&
        (
            (spadesFit == 12 && pts >= 15) ||
            (spadesFit == 11 && pts >= 17) ||
            (spadesFit == 10 && pts >= 20) ||
            (spadesFit ==  9 && pts >= 23) ||
            (spadesFit ==  8 && pts >= 25) ||
            (spadesFit ==  7 && pts >= 28)
        );
}

bool suitMakes(int fit, int pts, int contractLevel)
{
    int ptsTarget = (contractLevel - fit) * 2.5 + 35;
    return pts >= ptsTarget;
}
/*
bool northHasFiveSpadesAndTwoHeartsMakes(int p)
{
    return eastBidsWeakTwoInHearts() && twoHeartsMakes() && suitLength(north, 's') == 5 && points(north) == p;
}

bool northHasFiveSpadesAndTwoHeartsFails(int p)
{
    return eastBidsWeakTwoInHearts() && !twoHeartsMakes() && suitLength(north, 's') == 5 && points(north) == p;
}
*/
bool northHasFiveSpadesAndFourSpadesMakes(int p)
{
    int pts = points(north) + points(south);
    int spadesFit   = suitLength(north, 's') + suitLength(south, 's');
    return
        eastBidsWeakTwoInHearts() && suitLength(north, 's') == 5 && points(north) == p && suitMakes(spadesFit, pts, 4);
}

bool northHasFiveSpadesAndFourSpadesFails(int p)
{
    int pts = points(north) + points(south);
    int spadesFit   = suitLength(north, 's') + suitLength(south, 's');
    return
        eastBidsWeakTwoInHearts() && suitLength(north, 's') == 5 && points(north) == p && !suitMakes(spadesFit, pts, 4);
}

int bestNSfit()
{
    int spadesFit   = suitLength(north, 's') + suitLength(south, 's');
    int heartsFit   = suitLength(north, 'h') + suitLength(south, 'h');
    int diamondsFit   = suitLength(north, 'd') + suitLength(south, 'd');
    int clubsFit   = suitLength(north, 'c') + suitLength(south, 'c');
    int fit = max(spadesFit, heartsFit);
    fit = max(diamondsFit, fit);
    fit = max(clubsFit, fit);
    return fit;
}

int bestEWfit()
{
    int spadesFit   = suitLength(east, 's') + suitLength(west, 's');
    int heartsFit   = suitLength(east, 'h') + suitLength(west, 'h');
    int diamondsFit   = suitLength(east, 'd') + suitLength(west, 'd');
    int clubsFit   = suitLength(east, 'c') + suitLength(west, 'c');
    int fit = max(spadesFit, heartsFit);
    fit = max(diamondsFit, fit);
    fit = max(clubsFit, fit);
    return fit;
}

int longestSuit(HAND h)
{
    int spades   = suitLength(h, 's');
    int hearts   = suitLength(h, 'h');
    int diamonds   = suitLength(h, 'd');
    int clubs   = suitLength(h, 'c');
    int length = max(spades, hearts);
    length = max(diamonds, length);
    length = max(clubs, length);
    return length;
}

bool theTNTwhenNorthHasFiveSpadesAndEastBidsWeakTwoHearts(int fit)
{
    int fitNS = bestNSfit();
    int fitEW = bestEWfit();
    int TNT = fitNS + fitEW;
    return
        eastBidsWeakTwoInHearts() && suitLength(north, 's') == 5 && TNT == fit;
}

bool southPasses()
{
    return longestSuit(south) + points(south) < 16;
}

bool southPointCountWhenEastBidsSecond(int p)
{
    return
        eastBidsWeakTwoInHearts() && southPasses() && points(south) == p && points(north) == 23;
}

bool oneSpade(int p = 0)
{
    bool type1 = points(north) >= 15 && points(north) <= 19
        && suitLength(north, 's') == 4
        && suitLength(north, 'h') >= 2 && suitLength(north, 'h') <= 4
        && suitLength(north, 'd') >= 2 && suitLength(north, 'd') <= 4
        && suitLength(north, 'c') >= 2 && suitLength(north, 'c') <= 4;
    bool type2 = points(north) >= 10 && points(north) <= 16
        && suitLength(north, 's') == 6;
    return type1 || type2;
}

bool strong2NT(int p = 0)
{
    array<int, 4> a = {suitLength(north, 's'), suitLength(north, 'h'), suitLength(north, 'd'), suitLength(north, 'c')};
    sort(a.begin(), a.end());
    return
        points(north) >= 20 && points(north) <= 22 &&
        a[0] >= 1 && a[3] <= 5 &&
        a[0] + a[1] >= 4 &&
        a[2] + a[3] <= 9;
}

bool twoClubs(int p = 0)
{
    return
        points(north) >= 11 && points(north) <= 15 &&
        suitLength(north, 's') == 5 &&
        suitLength(north, 'h') <= 5 &&
        suitLength(north, 'd') <= 5 &&
        suitLength(north, 'c') <= 5;
}

bool oneDiamond(int p = 0)
{
    int type1 = points(north) >= 15 && points(north) <= 19 && suitLength(north, 'd') >= 4;
    int type2 = points(north) >= 12 && points(north) <= 49 && suitLength(north, 'd') >= 6;

    return type1 || type2;
}

bool twoDiamonds(int p = 0)
{
    bool type1 = points(north) >= 20;
    bool type2 = points(north) >= 17 && points(north) <= 20 &&
        (suitLength(north, 's') == 5 || suitLength(north, 's') == 6);
    return type1 || type2;
}

bool fourHeartsMakes(int p = 0)
{
    int pts = points(east) + points(west);
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 4) && points(east) == p;
}

bool threeHeartsMakes(int p = 0)
{
    int pts = points(east) + points(west);
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 3) && points(east) == p;
}

bool twoHeartsMakes(int p = 0)
{
    int pts = points(east) + points(west);
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 2) && points(east) == p;
}

bool oneHeartsMakes(int p = 0)
{
    int pts = points(east) + points(west);
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 1) && points(east) == p;
}

bool zeroHeartsMakes(int p = 0)
{
    int pts = points(east) + points(west);
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 0) && points(east) == p;
}

bool twoHeartsBid(int p = 0)
{
    return suitLength(east, 'h') >= 6 && points(east) == p;
}

bool TNT_if_twoHeartsMakes(int p = 0, int tnt = 0)
{
    int TNT = suitLength(east, 'h') + suitLength(west, 'h') + bestNSfit();
    int pts = points(east) + points(west);
    int fitNS = bestNSfit();
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 2) && points(east) == p && TNT == tnt;
}

bool TNT_if_oneHeartsMakes(int p = 0, int tnt = 0)
{
    int TNT = suitLength(east, 'h') + suitLength(west, 'h') + bestNSfit();
    int pts = points(east) + points(west);
    int heartFit   = suitLength(east, 'h') + suitLength(west, 'h');
    return suitLength(east, 'h') >= 6 && suitMakes(heartFit, pts, 1) && points(east) == p && TNT == tnt;
}

bool TNT_if_twoHeartsBid(int p = 0, int tnt = 0)
{
    int TNT = suitLength(east, 'h') + suitLength(west, 'h') + bestNSfit();
    return suitLength(east, 'h') >= 6 && points(east) == p && TNT == tnt;
}

bool combinedPointsIfWeakTwoBidInSecondPosition(int pe, int pw)
{
    return points(south) <= 11 && suitLength(east, 'h') >= 6 && points(east) == pe && points(west) == pw;
}

vector<T> v;
//int M = 100 * 1000 * 1000;
int M = 10 * 1000 * 1000;
//int M = 1000 * 1000;
//int M = 100 * 1000;


int main()
{
//    Register("weak two", eastBidsWeakTwoInHearts);
//    Register("NS pts", northSouthPointsAfterWeakTwoHearts, range(10, 30));
//    Register("NS fit", northSouthFitAfterWeakTwoHearts, range(7, 14));
//    Register("NS make 4 spades", northSouthCanMakeFourSpadesAfterWeakTwoHearts, range(7, 14));
//    Register("N has 5 spades and 5S makes", northHasFiveSpadesAndFourSpadesMakes, range(6, 20));
//    Register("N has 5 spades and 5S fails", northHasFiveSpadesAndFourSpadesFails, range(6, 20));
//    Register("N has 5 spades and 2H makes", northHasFiveSpadesAndTwoHeartsMakes, range(6,20));
//    Register("N has 5 spades and 2H fails", northHasFiveSpadesAndTwoHeartsFails, range(6,20));
//    Register("4H makes", fourHeartsMakes, range(0, 13));
//    Register("3H makes", threeHeartsMakes, range(0, 13));
//    Register("0H makes", zeroHeartsMakes, range(0, 13));
//    Register("TNT", theTNTwhenNorthHasFiveSpadesAndEastBidsWeakTwoHearts, range(6, 30));
//    Register("S points after 2H", southPointCountWhenEastBidsSecond, range(0, 12));
//    Register("1S opener", oneSpade);
//    Register("Strong 2NT", strong2NT);
//    Register("2C Opener", twoClubs);
//    Register("2D Opener", twoDiamonds);
//    Register("1D Opener", oneDiamond);

//    Register("TNT if 2H makes", TNT_if_twoHeartsMakes, range(0, 13), range(9, 25));
//    Register("TNT if 1H makes", TNT_if_oneHeartsMakes, range(0, 13), range(9, 25));
//    Register("TNT if 2H bid", TNT_if_twoHeartsBid, range(0, 13), range(9, 25));  // pts, TNT
    Register("combined pts EW if S passes first", combinedPointsIfWeakTwoBidInSecondPosition, range(3,11), range(0, 25));

    for(int i = 0; i < M; i++)
    {
        progress(i);
        tuple<HAND, HAND, HAND, HAND> hands = deal();
        north = std::get<0>(hands);
        east = std::get<1>(hands);
        south = std::get<2>(hands);
        west = std::get<3>(hands);
        for(auto& value: v)
        {
            auto& count = std::get<1>(value);
            auto& fn = std::get<2>(value);
            if(fn()) count++;
        }
    }
    
    for(auto& value: v)
    {
        auto& message = std::get<0>(value);
        auto& count = std::get<1>(value);
        cout << message << ", " << fixed << setprecision(2)
             << count << endl;
//        cout << message << ", " << fixed << setprecision(2)
//             << (100.0*count)/M << endl;
    }
}



