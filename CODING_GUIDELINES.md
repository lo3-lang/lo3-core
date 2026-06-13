# Coding Guidelines

This document defines the coding standard for this project.
All contributions must follow these rules.

---

## Standard

- **C11** only. Do not upgrade or downgrade.
- Do **not** use compiler-specific extensions or features.
  - Exception: `sizeof()` is allowed.
  - Exception: `asm()` is allowed for inline assembly (see Assembly section).
- The C preprocessor is allowed and encouraged where appropriate.

---

## Indentation

- Use **tabs**, not spaces.
- One tab = 8 spaces visual width.

---

## Spacing

Always put spaces around operators and after keywords:

```c
int a = b;       /* correct */
int a=b;         /* wrong   */
```

---

## Braces

Always use braces — never omit them, even for single-statement bodies.
Opening brace goes on the **same line** as the statement, closing brace on its own line:

```c
if (abc) {
	/* ... */
}
else {
	/* ... */
}
```

Functions follow the same rule:

```c
int main(void) {
	return 0;
}
```

Empty blocks use `{ }` or `{}` — pick one and stay consistent within a file:

```c
if (abc) { }
else { }
```

> **Note:** Prefer a `todo` comment over an intentionally empty block.
> Only use an empty block when you know exactly why it is empty.

---

# Spacing and Grouping

This document defines how blank lines are used to structure code in this project.
It extends the "Blank Lines and Code Grouping" section of the coding guidelines.

---

## Core Principle

A blank line marks a **semantic block change**.

Code that belongs to one thought — one "this does that" — stays together as a block.
As soon as the topic changes, even slightly, a blank line separates the blocks.

A second force works against pure grouping: **density**.
Code that looks too dense ("blobby") gets a blank line even when the topic has not changed.
When grouping and density conflict, avoid blobbiness.

Comments count as blocks too. A comment block is separated from unrelated code
like any other block.

---

## The ~2-Line Rule

Two blocks may be written together (no blank line between them) when the combined
code stays within **~2 lines**.

A "line" here is a unit of meaning — one "this does that".
An entire `if` block counts as **1**.

```c
*file = fopen(name, "r");

if (*file == NULL) {
	return -1;
}
```

Gray zone: a single short line may stand directly next to a short `if` block.
Both versions are acceptable — the separated one usually looks better.

---

## File Level

- The copyright / header comment block and the includes are two blocks that say
  completely different things → blank line between them.
- Blank line after the includes end.
- Critical globals (e.g. `volatile`) form their own block, separated from normal globals.
- Short related globals are grouped together:

```c
int currentLine = 0;
int lastLineOffset = 0;
```

- Exactly **one** blank line between functions.

---

## Function Header and Body

A blank line separates the function signature from the body — otherwise the header
blurs into the code:

```c
int pars_file(FILE *file) {

	char *line = NULL;
	...
```

Exception: a function whose whole body is **~2 lines or less** may start directly,
without the blank line.

Declarations at the top that serve one feature are grouped as a single block.
Writing them directly against the function header would make the header too blobby.
The blank line after them separates "creating the variables" from "doing the work".

A larger declaration area may be split into subgroups to loosen it up:

```c
	lo3_val result;
	result.type = type[0];
	char *end;

	int value;
	lo3_var *var;
```

---

## `if` Blocks

### Before an `if`

An `if` is separated from the code above it by a blank line.
A dense `if` (long condition) must **never** have a code line directly above it —
that only makes it denser.

### `if` next to `if`

Two `if` blocks stacked directly without a blank line are **always wrong**:

```c
if (a) {
}
if (b) {
}
```

There is always a blank line between `if {}` and `if {}`.

### After the closing `}`

A single short line (e.g. `return 0;`) may follow the closing brace directly —
as long as it is **not another `if`**, **not a `switch`**, and not too long:

```c
	if (len < 4 || strcmp(&name[len - 4], ".lo3") != 0) {

		lo3_error("File must end with .lo3\n", name);
		(void)(fclose((*file)));
		return -1;
	}
	return 0;
}
```

### Long conditions

From roughly **~25 characters** between the outer `(` and `)` — only the outer
parentheses count — the condition is blobby. A blank line follows the opening `{`,
even when the body would be short:

```c
	if (errno != 0 || end == &type[1] || idx < 0 || idx > INT_MAX) {

		lo3_error("Invalid g[] index", type);
		break;
	}
```

Short conditions get no inner blank line:

```c
	if (*fp == NULL) {
		lo3_error("Could not open file", name);
		return -1;
	}
```

### Heavy blocks

When the content of an `if` is visually heavy (e.g. a multi-line string in a call),
a blank line follows the whole block — otherwise the `if` looks even thicker.

---

## `else` / `else if`

`else` and `else if` go on the **next line** after the closing `}` — always.
No blank line in between, just the new line. If this was not done somewhere,
it is against the coding guidelines.

```c
	if (line[1] == '.') {
		ctx->startChar = line[2];
	}
	else if (line[1] == '{') {

		g_fasterInit(line);
	}
```

Inside an `else if` that starts after comments or feels loaded,
a blank line may loosen it up (as above).

### Chain limit

At most **3** `if` / `else if` in a chain. Beyond that, always use a `switch`.

---

## Loops

Same logic as `if`: a long loop header gets a blank line after the opening `{` —
the header together with the first lines would look too blobby:

```c
	while (lastLineOffset = ftell(file), GETLINE(&line, &len, file)) {

		currentLine++;
		line[strcspn(line, "\n")] = '\0';
```

---

## Labels

A `goto` label gets a blank line before it — it separates better:

```c
	int pos0 = ftell(file);

parsing:
	while (...) {
```

---

## `switch` / `case`

A blank line separates the `switch` from the declarations above it
(definitions end, switch begins).

### One-line cases

No blank line after the label:

```c
	case CNT_new:
		exec_new(a1, a2);
		break;
```

### Cases with more content

Blank line after the label:

```c
	case TYPE_string:

		result.value.string = &type[1];
		result.chooseType = 3;
		break;
```

A comment block counts as content — a case starting with comments
gets the blank line after the label too.

Cases are separated from each other by a blank line
(after `break;` / `return`, before the next `case`).

### `break` after a block

Inside a case, a blank line before `break;` after a multi-line block
can be omitted — but it looks better with it:

```c
		lo3_error("<num> is typeof integer!\nBut this value is not!", type);
		result.value.num = 0;
		result.chooseType = 0;

		break;
```

### After the `switch`

The `return` after a switch's closing `}` gets a blank line —
the return has nothing to do with `default`.
(This is different from `if`, where a single `return` follows the `}` directly.)

```c
	default:
		lo3_error("Unknown command!", "");
		break;
	}

	return -1;
```

---

## Gray Zones

This layer is partly taste. Some spots are "just barely ok" both ways —
e.g. three short assignments followed directly by `break;`.

When unsure, ask one question: **does it look blobby?**
If yes, add a blank line. Prefer air over density.

# condinue of the coding guidlines: main
## Nesting

- Maximum nesting depth: **4 levels**.
- A pair of `{}` counts as one level.
- A `switch` body counts as one level; individual `case` bodies inside it do **not** add a level.
- If you exceed 4 levels, restructure — extract a helper function.

---

## Names

### Files
Kebab-case: `lo3-getLine.c`, `control-flow.c`.

### Defines / Macros
ALL_CAPS: `MAX_SIZE`, `TRUE`, `FALSE`.

### Variables
camelCase: `varName`, `filePointer`.

Single-character names are allowed but carry risk — the reader may not understand them.
Avoid random or meaningless names (`sjdi`, `xqz`).

Common short names that are always acceptable:
- `buf` — a buffer
- `fp` — file pointer
- `stack` — a manually managed stack
- Any other well-known abbreviation that is unambiguous in context

### Types
When you need a custom type, use the `_t` suffix: `myType_t`.

### Functions
`<module>_camelCaseName()`, where the module prefix matches the file name shortened to its semantic group:

```c
lo3_parse()    /* from lo3 / parsing */
var_create()   /* from variable.c    */
```

---

## `const` vs `#define`

Prefer `#define` over `const`.
Use `const` only when it is genuinely necessary (e.g., a pointer that must carry a type-qualified contract).

---

## Type Qualifiers

Use `restrict` when two pointer parameters can **never** alias, but only when it is truly the case:

```c
void copy(char *restrict dst, const char *restrict src);
```

Do not add `restrict` speculatively.

---

## Floating-Point Types

Prefer `double` over `float`.

Exception: when memory is critical — low-level or embedded code where every byte matters.
In those cases `float` (or even smaller types) is appropriate.

---

## `(void)` Cast

Cast the return value to `(void)` when you intentionally skip checking it,
but **only** when you are sure it is safe to ignore:

```c
(void)printf("hello\n");
(void)fclose(fp);
(void)fseek(fp, 0, SEEK_SET);
```

Rules:
- I/O and OS operations that return something: cast to `(void)` (if `printf` fails you likely cannot do I/O at all — it is not your problem).
- Heap allocations (`malloc`, `calloc`, `realloc`): **must** be checked — never cast to `(void)`.
- `free()` is already `void` — no cast needed.

---

## Error Handling

- Return `-1` when a function has been called incorrectly or when propagating an error makes sense.
- Do not always return `-1` — for functions returning `char` or other narrow types, use a type-appropriate sentinel.
- Use the project error helpers:
  - `lo3_error()` — fatal / hard errors
  - `lo3_warn()` — non-fatal warnings
  - `PRINTLI` — debug print (planned; outputs interpreter state for debugging)

---

## `goto`

Use `goto` for cleanup and early-exit patterns.
Rules:
- Only jump **forward** (down) in the function — never upward.
- "Public" cleanup at the end of a function is allowed when it provides a clear benefit.

```c
void sampleFunc(void) {
	if (TRUE) {
		goto err;
	}

	/* normal work */

err:
	/* cleanup */
}
```

Jumping forward to a return point at the bottom of a function is acceptable,
but only when there is a clear reason to do it that way.

---

## Comments

Single-line comments use `//` only. `/*` and `*/` are **not** allowed for single-line comments:

```c
// this is correct
/* this is wrong for a single-line comment */
```

Multi-line — use `/*` / `*/` with a leading `*` on every body line.
Write only as many lines as needed:

```c
/*
 * first line of explanation
 * second line of explanation
 */
```

Do **not** write on the `/*` opening line or the `*/` closing line.

### `todo` comments

```c
// todo: <short description>
// ///// More Informations /////
// <longer explanation and, if needed, a step-by-step guide>
```

This is the **only** case where a multi-line `//` comment block is used.
Always use this exact format for todos.

---

## Assembly

- A few lines of inline assembly: use `asm()`.
- Larger routines that need many registers or complex control flow: write a separate `.S` file and bind it.
- Do not mix sizeable assembly logic into `.c` files.

---

## Header Guards

Prefer `#pragma once`:

```c
#pragma once
```

You may use traditional `#ifndef` guards, but `#pragma once` is the preferred style.

---

## Boolean Values

Use `TRUE` and `FALSE` from `cf-define.h` wherever the context is boolean.
`1` and `0` are acceptable for purely numeric comparisons.

---

## Section Dividers in Headers

Multi-purpose header files (shared across several `.c` files) must divide their sections with:

```c
///// <section name> /////
```

Example:

```c
///// from var.c /////
```

This rule applies **only** to multi-purpose headers — single-purpose headers do not need dividers.
