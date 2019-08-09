CC := clang++
SOURCES := $(wildcard *.cpp)
OBJECTS := $(SOURCES:.cpp=.o)

CFLAGS = -g -std=c++17

all: weakTwos.exe

$(OBJECTS): %.o: %.cpp
	$(CC) -c $(CFLAGS) $< -o $@ $(LFLAGS)

weakTwos.exe: $(OBJECTS)
	$(CC) $(CFLAGS) $(LFLAGS) $(OBJECTS) -o $@

clean:
	rm -f *.exe *.o
	rm -rf *.exe.dSYM
	




