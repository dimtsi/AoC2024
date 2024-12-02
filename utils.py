import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Literal, Optional

from aocd import submit


def submit_answer(answer, part="a", dt: Optional[datetime] = None):
    if not dt:
        today = datetime.today()
        day, year = today.day, today.year
    else:
        day, year = dt.day, dt.year

    submit(answer=answer, part=part, day=day, year=year)


def run_and_submit(
    filename: str,
    part: Literal["a", "b"],
    runner: Callable,
    expected: Optional[Any] = None,
    submit: bool = False,
    dt: Optional[datetime] = None,
):
    sample = True if "sample" in filename else False

    res = runner(filename)

    if sample:
        if expected:
            assert (
                res == expected
            ), f"Answer{part.upper()} incorrect: Actual: {res}, Expected: {expected}"

            print(f"sample{part.upper()} correct")

    print(
        f"{filename.split('/')[-1].upper()} part{part.upper()} answer:\n{res}\n"
    )

    if submit:
        if dt is None:
            raise ValueError("You must provide datetime to be able to submit")
        submit_answer(res, part, dt)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(
            f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds"
        )
        return result

    return timeit_wrapper
