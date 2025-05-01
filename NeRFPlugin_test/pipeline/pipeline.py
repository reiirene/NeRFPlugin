from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class Pipeline(Generic[T, U]):
    def __init__(self, func: Callable[[T], U]) -> None:
        self.func = func

    def add_step(self, func: Callable[[U], V]) -> "Pipeline[T, V]":
        """Add a step to the pipeline."""
        return Pipeline(lambda x: func(self.func(x)))

    def execute(self, input: T) -> U:
        """Execute the pipeline with the given input."""
        return self.func(input)


class PipelineBuilder:
    def add_step(self, func: Callable[[T], U]) -> Pipeline[T, U]:
        return Pipeline(func)
