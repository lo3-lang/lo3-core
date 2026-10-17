# lo3-core — plain GNU Makefile (replaces CMakeLists.txt)
#
#   make                 release build -> bin/lo3
#   make debug           -O0 -g, sanitizers on Linux/macOS
#   make test            build + run unit tests
#   make run             build + ./bin/lo3 test.lo3
#   make clean
#
#   Overrides: make CC=clang  |  make OPT=-O3  |  make V=1 (verbose)

# ---------------------------------------------------------------- toolchain
ifeq ($(origin CC),default)
CC := gcc
endif

STD      := -std=gnu11
WARN     := -Wall -Wextra -Wno-pointer-sign -Wno-unused-parameter
OPT      ?= -O2
CPPFLAGS += -D_DEFAULT_SOURCE -D_POSIX_C_SOURCE=200809L -Iinclude
DEPFLAGS  = -MMD -MP

# ---------------------------------------------------------------- platform
ifeq ($(OS),Windows_NT)
    PLATFORM := windows
    EXE      := .exe
    NPROC    := $(NUMBER_OF_PROCESSORS)
else
    UNAME    := $(shell uname -s)
    EXE      :=
    ifeq ($(UNAME),Darwin)
        PLATFORM := macos
        NPROC    := $(shell sysctl -n hw.ncpu)
    else
        PLATFORM := linux
        LDLIBS   += -ldl
        NPROC    := $(shell nproc 2>/dev/null || echo 1)
    endif
endif

# parallel by default (override with make -j1)
MAKEFLAGS += -j$(NPROC)

# quiet output unless V=1
ifeq ($(V),1)
    Q :=
else
    Q := @
endif

# ---------------------------------------------------------------- sources
BUILD    := build
BIN      := bin/lo3$(EXE)

SRC      := $(wildcard src/*.c)
OBJ      := $(SRC:%.c=$(BUILD)/%.o)

CORE_OBJ := $(filter-out $(BUILD)/src/main.o,$(OBJ))

# ---------------------------------------------------------------- tests
TEST_INC := -Isrc/internal -Itest/unit/unity
UNITY    := $(BUILD)/test/unit/unity/unity.o
TEST_SRC := $(wildcard test/unit/test_*.c)
TESTS    := $(TEST_SRC:test/unit/%.c=$(BUILD)/test/%$(EXE))

# ---------------------------------------------------------------- rules
.PHONY: all debug test run clean info
.SECONDARY:   # keep intermediate test objects

all: $(BIN)

debug: OPT := -O0 -g3
ifneq ($(PLATFORM),windows)
debug: OPT += -fsanitize=address,undefined
debug: LDFLAGS += -fsanitize=address,undefined
endif
debug: $(BIN)

$(BIN): $(OBJ)
	@mkdir -p $(@D)
	@echo "  LD    $@"
	$(Q)$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

$(BUILD)/%.o: %.c
	@mkdir -p $(@D)
	@echo "  CC    $<"
	$(Q)$(CC) $(STD) $(WARN) $(CPPFLAGS) $(OPT) $(CFLAGS) $(DEPFLAGS) -c -o $@ $<

# test sources need the internal + unity include paths
$(BUILD)/test/%.o: CPPFLAGS += $(TEST_INC)

$(BUILD)/test/%$(EXE): $(BUILD)/test/unit/%.o $(CORE_OBJ) $(UNITY)
	@echo "  LD    $@"
	$(Q)$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

test: $(TESTS)
	@for t in $(TESTS); do echo "== $$t"; ./$$t || exit 1; done

run: $(BIN)
	./$(BIN) test.lo3

clean:
	rm -rf $(BUILD) $(BIN)

info:
	@echo "platform: $(PLATFORM)  cc: $(CC)  jobs: $(NPROC)"
	@echo "sources:  $(SRC)"
	@echo "tests:    $(TESTS)"

# auto-generated header dependencies
-include $(OBJ:.o=.d) $(UNITY:.o=.d) $(TEST_SRC:%.c=$(BUILD)/%.d)
