from typing import List, Generic, Callable, TypeVar

from .objects import Object


T = TypeVar('T', bound=Object)

class Template(Generic[T]):
    def __init__(self, factory: Callable[..., List[T]], **fixed_kwargs):
        self.factory = factory
        self.fixed = fixed_kwargs

    def create(self, **kwargs) -> List[T]:
        merged = {**self.fixed, **kwargs}
        return self.factory(**merged)

    def __call__(self, **kwargs) -> List[T]:
        return self.create(**kwargs)

    def map(self, func: Callable[[T], T]) -> 'Template[T]':
        def new_factory(**kwargs):
            objs = self.factory(**{**self.fixed, **kwargs})
            return [func(obj) for obj in objs]
        return Template(new_factory)


def template(**fixed_kwargs) -> Callable[[Callable[..., List[Object]]], Template]:
    def decorator(func: Callable[..., List[Object]]) -> Template:
        return Template(func, **fixed_kwargs)
    return decorator

