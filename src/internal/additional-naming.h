#pragma once

// just some values for the exec,
// to not use some random values.
#define ATYPE_num 0x0
#define ATYPE_var 0x1
#define ATYPE_array 0x2
#define ATYPE_string 0x3

// sleep(ms) macro
#ifdef _WIN32
#include <windows.h>
#define ASLEEP(ms) Sleep(ms);

#else // linux
#include <unistd.h>
#define ASLEEP(ms) usleep((ms) * 1000) // mic sec -> ms

#endif
