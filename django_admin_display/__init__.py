from typing import Callable, Optional, TypeVar, Union

import django
from django.db.models.expressions import BaseExpression

ReturnType = TypeVar('ReturnType')
FuncType = Callable[..., ReturnType]
Func = TypeVar('Func', bound=FuncType)


def admin_display(
    admin_order_field: Optional[Union[str, BaseExpression]] = None,
    allow_tags: Optional[bool] = None,  # deprecated in django >= 2.0
    boolean: Optional[bool] = None,
    empty_value_display: Optional[str] = None,
    short_description: Optional[str] = None,
) -> Callable[[Func], Func]:
    """
    Extend method with special attributes for use by the django admin.
    """

    def wrapper(func: Func) -> Func:
        if admin_order_field is not None:
            setattr(func, 'admin_order_field', admin_order_field)
        if allow_tags is not None:
            if django.VERSION[:2] > (1, 11):
                raise AttributeError(
                    "`allow_tags` is not supported by django > 2.0",
                )
            setattr(func, 'allow_tags', allow_tags)
        if boolean is not None:
            setattr(func, 'boolean', boolean)
        if empty_value_display is not None:
            setattr(func, 'empty_value_display', empty_value_display)
        if short_description is not None:
            setattr(func, 'short_description', short_description)
        return func

    return wrapper
