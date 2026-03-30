// Copyright (c) 2026 seesee010
// Read the License file for more informations about the license.

#include "../include/additional-naming.h"
#include "../include/core.h"
#include "../include/specific-language.h"
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

/*
 * algo:
 * if the type of a1 is the same type, else lo3_error.
 * assign a1 = a2; if everything is correct!
 */
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

	// check for type diff
	if (a2.chooseType != a1.chooseType) {
		lo3_error("The types of arg0 and arg1 are not the same!\n"
		          "Please check if you define your var as the asociated type of arg1",
		          ""); // "": returns an line num!
		return;
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

	char buf[64];
	char *name;

	if (!a1.chooseType) {
		snprintf(buf, sizeof(buf), "%d", a1.value.num);
		name = buf;
	} else {
		name = a1.value.string;
	}

	printf("%s\n", name);
}

void exec_in(lo3_val a1, lo3_val a2, char array[2]) {

	char buf[64]; // max limit of pars_resv();
	char *res;

	char numNameBuf[64];
	char *name;

	res = fgets(buf, sizeof(buf), stdin);

	if (res == NULL) {
		lo3_error("Something went wrong while reading the stdin stream.\n"
		          "Please check if you done anything wrong...",
		          buf);
		return;
	}

	// parse the '\n' away
	buf[strcspn(buf, "\n")] = '\0';

	lo3_val temp = pars_resv(buf);

	// transform lo3_val -> lo3_var
	lo3_var newVar;
	newVar.type = temp.chooseType;

	if (!temp.chooseType) {
		newVar.value.num = temp.value.num;
	} else {
		newVar.value.string = temp.value.string;
	}

	// correct the a1.~type
	if (!a1.chooseType) {
		snprintf(numNameBuf, sizeof(numNameBuf), "%d", a1.value.num);
		name = numNameBuf;

	} else {
		name = a1.value.string;
	}

	var_set(name, newVar);
}
