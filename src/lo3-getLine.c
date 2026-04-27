#include "./internal/core.h"

#ifdef _WIN32

int lo3_getLine(char **lineptr, size_t *n, FILE *stream) {
	if (!*lineptr || !*n) {
		*lineptr = malloc(*n = 128);
		if (!*lineptr) return -1;
	}

	size_t pos = 0;
	int c;

	while ((c = fgetc(stream)) != EOF) {
		if (pos + 2 > *n) {
			char *tmp = realloc(*lineptr, *n *= 2);
			if (!tmp) return -1;
			*lineptr = tmp;
		}
		(*lineptr)[pos++] = (char)c;
		if (c == '\n') break;
	}

	if (!pos) return -1;

	(*lineptr)[pos] = '\0';
	return (int)pos;
}

#endif
