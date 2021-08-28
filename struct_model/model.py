from struct import Struct
from typing import Iterable, TypeVar

import ujson

from .types import *

__all__ = [
    'StructModel',
]

T = TypeVar('T', bound='StructModel')


# TODO: add __init__ hints for IDE somehow
class StructModel:
    """
    Base dataclass like model for python's built-in struct.
    Inherit this class with annotated attributes to create new model

    Example:

        class CustomForm(StructModel, byte_order='big'):
            username: char[24]
            balance: uint4
    """
    byte_order: O_ALL_LITERAL
    _fields: dict[str, _T_Type]
    struct: Struct

    def __init__(self, *args, **kwargs):
        for k, v in zip(self._fields.keys(), args):
            setattr(self, k, v)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __init_subclass__(cls, byte_order: T_ByteOrder = O_NETWORK):
        """
        :param byte_order: big |
        :type byte_order:
        """
        cls.byte_order = parse_bo(byte_order)
        cls._fields = {}
        struct = byte_order
        for _field, _type in cls.__annotations__.items():
            if not isinstance(_type, type) or not issubclass(_type, _Type):
                continue
            cls._fields[_field] = _type
            struct += f'{_type.amount}{_type.key}'
        cls.struct = Struct(struct)
        cls.__slots__ = tuple(cls._fields.keys())

    def iter_keys(self) -> Iterable[str]:
        for field in self._fields.keys():
            yield field

    def iter_values(self) -> Iterable[int | float | str | bool | bytes | None]:
        for field in self._fields.keys():
            yield getattr(self, field, None)

    def iter_items(self) -> Iterable[tuple[str, int | float | str | bool | bytes | None]]:
        yield from zip(self.iter_keys(), self.iter_values())

    def _dict_items(self):
        for key, val in self.iter_items():
            if isinstance(val, StructModel):
                yield key, val.dict()
            else:
                yield key, val

    def dict(self) -> dict:
        return dict(self._dict_items())

    @classmethod
    def from_dict(cls, obj: dict) -> T:
        return cls(**obj)

    def json(self) -> str:
        return ujson.dumps(self.dict(), ensure_ascii=False, escape_forward_slashes=False)

    @classmethod
    def from_json(cls, obj: str | bytes) -> T:
        return cls(**ujson.loads(obj))

    def pack(self) -> bytes:
        return self.struct.pack(*(
            _type.to_struct_value(val)
            for val, _type in zip(self.iter_values(), self._fields.values())
        ))

    @classmethod
    def unpack(cls, buff: bytes | bytearray | memoryview) -> T:
        return cls(*(
            _type.to_python_value(val)
            for val, _type in zip(cls.struct.unpack(buff), cls._fields.values())
        ))

    dump = dumps = pack
    load = loads = unpack
