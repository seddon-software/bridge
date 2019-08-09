/*
This program calculates the fit after a 2NT opening showing two 5 card suits
*/

#include "Bridge.h"
#include "Patterns.h"

using namespace std;

HAND north;
HAND east;
HAND south;
HAND west;

tuple<HAND, HAND, HAND, HAND> deal()
{
// setup engine
	static std::random_device rdev{};
	static std::default_random_engine engine{rdev()};

// Manufacture a deck of cards:
	std::array<Card, 52> deck{};
	std::iota(deck.begin(), deck.end(), 0);

// Shuffle the deck:
	std::shuffle(deck.begin(), deck.end(), engine);
	std::shuffle(deck.begin(), deck.end(), engine);
	std::shuffle(deck.begin(), deck.end(), engine);

// Display each card in the shuffled deck:
	auto suit = []( Card c ) { return "shdc"[c/13]; };
	auto rank = []( Card c ) { return "AKQJX98765432"[c%13]; };

// Assign cards
	HAND north, east, south, west;
	std::copy(&deck[ 0], &deck[13], &north[0]);
	std::copy(&deck[13], &deck[26], &east[0]);
	std::copy(&deck[26], &deck[39], &south[0]);
	std::copy(&deck[39], &deck[52], &west[0]);

	return std::make_tuple(north, east, south, west);
}

int suitLength(const HAND& hand, char suit)
{
	auto suitOf = []( Card c ) { return "shdc"[c/13]; };

	int count = 0;
	for(Card card : hand)
	{
		if(suitOf(card) == suit) count++;
	}
	return count;
}

int suitLength(char suit)
{
	return suitLength(north, suit);
}

int points(const HAND& hand)
{
    int pts = 0;
    for(Card card : hand)
    {
        card = 4 - card % 13;
        if(card > 0) pts += card;
    }
    return pts;
}

int points()
{
    return points(north);
}

void progress(int i)
{
    if(i % (N/10) == 0) cout << (100*i)/N << "%, ";
    cout.flush(); 
    if(i == N - 1) cout << endl;
}


//int N = 500;
//int N = 100000;
int N = 1000000;
//int N = 10000000;

int main()
{
	vector<Results> items;
    items.push_back(Results("east bids weak 2 in hearts", eastBidsWeakTwoInHearts));
    items.push_back(Results("east's Weak 2 goes down (6)", eastsWeakTwoGoesDown6));
    items.push_back(Results("east's Weak 2 goes down (7)", eastsWeakTwoGoesDown7));
    items.push_back(Results("east's Weak 2 goes down (8)", eastsWeakTwoGoesDown8));
    items.push_back(Results("east's Weak 2 goes down (9)", eastsWeakTwoGoesDown9));
    items.push_back(Results("east/west have fit (6)", eastWestFit6));
    items.push_back(Results("east/west have fit (7)", eastWestFit7));
    items.push_back(Results("east/west have fit (8)", eastWestFit8));
    items.push_back(Results("east/west have fit (9)", eastWestFit9));
    items.push_back(Results("east/west have fit (10)", eastWestFit10));
    items.push_back(Results("east/west have fit (11)", eastWestFit11));
    items.push_back(Results("east's weak two goes down and we have seven card fit", eastsWeakTwoGoesDownAndWeHaveSevenCardFit));
    items.push_back(Results("east's weak two goes down and we have eight card fit", eastsWeakTwoGoesDownAndWeHaveEightCardFit));
    items.push_back(Results("east's weak two goes down and we have nine card fit", eastsWeakTwoGoesDownAndWeHaveNineCardFit));
    items.push_back(Results("east's weak two goes down and we have ten card fit", eastsWeakTwoGoesDownAndWeHaveTenCardFit));

	// loop round checking patterns
	for(int i = 0; i < N; i++)
	{
        progress(i);
		tuple<HAND, HAND, HAND, HAND> hands = deal();
		north = std::get<0>(hands);
		east = std::get<1>(hands);
		south = std::get<2>(hands);
		west = std::get<3>(hands);
        for(auto& value: items)
        {
             value.check();
        }
    }
    
    // print out results
    cout << "probabilities of various bids occuring:" << endl << endl;
    for(auto const& value: items)
    {
         value.show();
    }
}


