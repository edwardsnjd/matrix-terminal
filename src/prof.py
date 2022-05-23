"""
Simple profiling script for the program.
"""

from pstats import SortKey
from tempfile import NamedTemporaryFile
import cProfile
import pstats


from main import loop


def main():
    # Profile something
    p = get_profiling_stats(lambda: loop(200))

    # Top down longest running (not too surprising)
    p.sort_stats(SortKey.CUMULATIVE).print_stats(15)

    # Bottom up longest running (shows up hot spots)
    p.sort_stats(SortKey.TIME).print_stats(15)


def get_profiling_stats(fn):
    """Profile the given callable and return the profiling stats"""
    with NamedTemporaryFile() as profiling_data:
        # Write results to temporary file and clean up after
        file_path = profiling_data.name

        cProfile.runctx('fn()', globals(), locals(), file_path)

        return pstats.Stats(file_path)


if __name__ == "__main__":
    main()
