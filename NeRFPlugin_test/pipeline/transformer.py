from typing import Protocol, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)
U_co = TypeVar("U_co", covariant=True)


class Transformer(Protocol[T_contra, U_co]):
    def transform(self, input: T_contra) -> U_co:
        """Transform the input data."""
        ...

    def __call__(self, input: T_contra) -> U_co:
        """Make the transformer callable."""
        ...
        return self.transform(input)
