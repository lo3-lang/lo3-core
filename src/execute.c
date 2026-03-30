// Copyright (c) 2026 seesee010
// Read the License file for more informations about the license.

#include "../include/additional-naming.h"
#include "../include/core.h"
#include "../include/var.h"
#include <stdio.h>

void exec_new(lo3_val a1, lo3_val a2, char array[2]) {

	char buf[64];
	char *name;

	if (!a1.chooseType) {

		snprintf(buf, sizeof(buf), "%d", a1.value.num);
		lo3_warn("Are you sure you want to set the name as a number?", buf);
		name = buf;
	} else {
		name = a1.value.string;
	}

	// get the type
	int type = (!a2.chooseType) ? a2.value.num : atoi(a2.value.string);

	// duplication check
	if (var_find(name) != -1) {
		lo3_error("Variable already exists!", name);
		return;
	}

	if (type != 0 && type != 3) {

		snprintf(buf, sizeof(buf), "%d", type);
		lo3_warn("Variable type might not be num or string!", buf);
	}

	var_create(name, type);
}

void exec_free(lo3_val a1, lo3_val a2, char array[2]) {

	char buf[64];
	char *name;

	if (!a1.chooseType) {
		snprintf(buf, sizeof(buf), "%d", a1.value.num);
		lo3_warn("Are you sure you want to delete some var called:\nDoing it anyways... ",
		         buf);
		name = buf;
	} else {
		name = a1.value.string;
	}

	// ignore arg1

	var_free(name);
}

void exec_asn(lo3_val a1, lo3_val a2, char array[2]) {

	char buf[64];
	char *name;

	if (!a1.chooseType) {
		snprintf(buf, sizeof(buf), "%d", a1.value.num);
		lo3_warn("Please verify that you really thought that you can assign a VALUE some "
		         "VALUE!",
		         buf);
		name = buf;
	} else {
		name = a1.value.string;
	}

	// string
	if (a2.chooseType) {
	}
}
void exec_add(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_sub(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_mul(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_div(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_jmp(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_call(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_callS(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_label(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_out(lo3_val a1, lo3_val a2, char array[2]) {
}

void exec_in(lo3_val a1, lo3_val a2, char array[2]) {
}
