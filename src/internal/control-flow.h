#pragma once

// true and false so it is more fancy!
#define TRUE 1
#define FALSE 0
#define ARRAY_SIZE 254
#define BUF_SIZE 255

extern char rush;
extern char rush_target[256];
extern char isWarped;
extern int lastLineOffset;

typedef struct lo3_label {
	char *names[ARRAY_SIZE];

	// -1 tracks the next pos
	int pos[ARRAY_SIZE]; // could be fixed by importing size_t
	int nextFreePos;     // if nextFreePos = ARRAY_SIZE, array is full!
} lo3_label;

typedef struct {
	char nextFreePos;
	char values[ARRAY_SIZE];
} lo3_stack;

extern lo3_label cf;

int cf_addLabel(const char *name, const int pos);
int cf_jumpToLabel(const char *name);
int cf_findLabel(const char *name);
int cf_getPos(const char *name);

void cf_setCursorPos(const int i);
int cf_getCursorPos(void);

// parsing
void cf_fasterLabel(char line[255]);
void cf_fasterJumptoLabel(char line[255]);

// call
void cf_pop(lo3_stack stack);
void cf_push(lo3_stack stack);