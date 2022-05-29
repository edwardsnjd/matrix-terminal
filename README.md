matrix-terminal
===============

A toy Matrix digital rain clone.

To run locally, you'll need to have the following available:
- `python` (v3+)
- `mypy`
- `tput`
- `echo`

Usage
-----

`./matrix-terminal`

Notes
-----

The performance of the naive implementation that looks up the
character position string using `tput` each time is quite poor.  Since
those characters do not change they can be cached for the lifetime of
the program, using the `@cache` decorator in python.
