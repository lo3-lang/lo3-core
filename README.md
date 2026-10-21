# lo3 programming language

![License](https://img.shields.io/github/license/lo3-lang/lo3-core)
![Release](https://img.shields.io/github/v/release/lo3-lang/lo3-core)
![Build](https://img.shields.io/github/actions/workflow/status/lo3-lang/lo3-core/release.yml)
![Language](https://img.shields.io/badge/written%20in-C-blue)
![Platform](https://img.shields.io/badge/platform-linux%20|%20windows-lightgrey)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/lo3-lang/lo3-core)

> [!NOTE]
> Claude Code is not used for the core func of this repo.
> Only for bug fixes, test/*, ...

## What is this language about?
lo3 is a token based interpreted programming language written in C.

## Website
See [Main Website](https://lo3-lang.github.io)

See [learn-the-syntax](https://lo3-lang.github.io/learn-the-syntax/) for examples and documentation.

## Run lo3 at your own machine

```bash
lo3 {FILENAME}
```
This will start the interpreter and run your code.

## Compile it yourself

```bash
make install
```

## Tests
Tests are written in C++, Rust and Python to avoid language-level bias when testing a C core.

Run all tests:

```bash
make -k test
```

## License

[LICENSE](./LICENSE)
