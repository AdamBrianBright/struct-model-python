from enum import Enum
from typing import Literal, TYPE_CHECKING, Type, TypeVar, Union

__all__ = [
    'O_DEFAULT',
    'O_NATIVE',
    'O_LITTLE',
    'O_SMALL',
    'O_BIG',
    'O_NETWORK',
    'O_ALL',
    'O_ALL_LITERAL',
    'ByteOrder',
    'T_ByteOrder',
    'parse_bo',
    '_T_Type',
    '_Type',
    'DynamicLength',
    'Padding',
    'Bool',
    'Char',
    'Bytes',
    'PascalBytes',
    'Size',
    'uSize',
    'Int1',
    'uInt1',
    'Int2',
    'uInt2',
    'Int4',
    'uInt4',
    'Int8',
    'uInt8',
    'Float2',
    'Float',
    'Double',
    'String',
    'PascalString',
]
# region Byte Order
# see: https://docs.python.org/3.9/library/struct.html#byte-order-size-and-alignment
ENCODING = 'utf-8'

O_DEFAULT = '@'
O_NATIVE = '='
O_LITTLE = O_SMALL = '<'
O_BIG = '>'
O_NETWORK = '!'
O_ALL = list('@=<>!')
O_ALL_LITERAL = Union[Literal['@', '=', '<', '>', '!'], str]


class ByteOrder(Enum):
    default = '@'
    native = '='
    little = '<'
    small = '<'
    big = '>'
    network = '!'


T_ByteOrder = Union[ByteOrder, O_ALL_LITERAL, Literal['big', 'small', 'little', 'network']]


def parse_bo(bo: T_ByteOrder = None) -> O_ALL_LITERAL:
    if bo is None:
        return '!'
    if isinstance(bo, ByteOrder):
        return bo.value
    if isinstance(bo, str):
        bo = bo.lower()
        if bo == 'big':
            return '>'
        elif bo in ['small', 'little']:
            return '<'
        elif bo == 'network':
            return '!'
        elif bo in O_ALL:
            return bo
    raise TypeError(f'Provided invalid ByteOrder type "{type(bo)}<{bo!r}>"')


# endregion


# region Format characters
# see: https://docs.python.org/3.9/library/struct.html#format-characters

# <editor-fold defaultstate="collapsed" desc="Type basics">

class _Type:
    key: str
    byte_orders: Union[O_ALL_LITERAL, tuple[O_ALL_LITERAL]] = '*'

    def __init_subclass__(cls, key: str = '', byte_orders: str = '*'):
        assert key, f'Unbound key {cls}'
        cls.key = key
        cls.byte_orders = '*'

    @classmethod
    def to_struct_value(cls, v):
        raise NotImplementedError

    @classmethod
    def to_python_value(cls, v):
        raise NotImplementedError

    @classmethod
    def supports(cls, bo: O_ALL_LITERAL):
        return cls.byte_orders == '*' or cls.byte_orders == ['*'] or bo in cls.byte_orders


_T_Type = Type[_Type]

_Dyn = TypeVar('_Dyn', bound='DynamicLength')


class DynamicLength(_Type, key='x'):
    amount: int = 1

    @classmethod
    def mutate(cls, amount: int = 1, **kwargs) -> Union[type, Type[_Dyn]]:
        return type(cls.__name__, (cls, DynamicLength, _Type), {'amount': amount, **kwargs}, key=cls.key)

    @classmethod
    def to_struct_value(cls, v):
        raise NotImplementedError

    @classmethod
    def to_python_value(cls, v):
        raise NotImplementedError


# </editor-fold>


# region Padding
if TYPE_CHECKING:
    _Padding = None
else:
    class _Padding(DynamicLength, _Type, key='x'):
        @classmethod
        def to_struct_value(cls, v):
            return bytes(cls.amount)

        @classmethod
        def to_python_value(cls, v):
            return None


def Padding(amount: int = 1) -> Type[None]:  # noqa
    return _Padding.mutate(amount)


# endregion


# region Bool Types
if TYPE_CHECKING:
    Bool = bool
else:
    class Bool(int, _Type, key='?'):
        @classmethod
        def to_struct_value(cls, v):
            return bool(v)

        @classmethod
        def to_python_value(cls, v):
            return bool(v)

# endregion

# region Byte types

if TYPE_CHECKING:
    Char = _Bytes = _PascalBytes = bytes
else:
    class Char(bytes, _Type, key='c'):
        @classmethod
        def to_struct_value(cls, v):
            if not len(v) == 1:
                raise ValueError('Char accepts only one symbol')
            return v

        @classmethod
        def to_python_value(cls, v):
            return bytes(v)


    class _Bytes(bytes, DynamicLength, _Type, key='s'):
        strip_null: bool

        @classmethod
        def to_struct_value(cls, v):
            if len(v) > cls.amount:
                raise ValueError(f'Max length exceeded: {len(v)}/{cls.amount}')
            return bytes(v)

        @classmethod
        def to_python_value(cls, v):
            v = bytes(v)
            if cls.strip_null:
                v = v.replace(b'\x00', b'')
            return v


    class _PascalBytes(_Bytes, key='p'):
        pass


def Bytes(amount: int = 1, strip_null: bool = True) -> Type[bytes]:  # noqa
    return _Bytes.mutate(amount, strip_null=strip_null)


def PascalBytes(amount: int = 1, strip_null: bool = True) -> Type[bytes]:  # noqa
    return _PascalBytes.mutate(amount, strip_null=strip_null)


# endregion

# region Integer types

if TYPE_CHECKING:
    _Size = _uSize = int
    Int1 = uInt1 = int
    Int2 = uInt2 = int
    Int4 = uInt4 = int
    Int8 = uInt8 = int
else:
    class _Size(int, DynamicLength, _Type, key='n', byte_orders=(O_DEFAULT, O_NATIVE)):
        @classmethod
        def to_struct_value(cls, v):
            v = int(v)
            ln = v.bit_length()
            if ln > cls.amount * 8:
                raise ValueError(f'Max length exceeded: {ln // 8}/{cls.amount}')
            return int(v)

        @classmethod
        def to_python_value(cls, v):
            return int(v)


    class _uSize(_Size, key='N', byte_orders=(O_DEFAULT, O_NATIVE)):  # noqa
        pass


    class Int1(int, _Type, key='b'):
        byte_len = 1

        @classmethod
        def to_struct_value(cls, v):
            v = int(v)
            ln = v.bit_length()
            if ln > cls.byte_len * 8:
                raise ValueError(f'Max length exceeded: {ln // 8}/{cls.byte_len}')
            return int(v)

        @classmethod
        def to_python_value(cls, v):
            return int(v)


    class uInt1(int, _Type, key='B'):  # noqa
        byte_len = 1

        @classmethod
        def to_struct_value(cls, v):
            v = int(v)
            ln = v.bit_length()
            if ln > 8:
                raise ValueError(f'Max length exceeded: {ln // 8}/{cls.byte_len}')
            return int(v)

        @classmethod
        def to_python_value(cls, v):
            return int(v)


    class Int2(Int1, key='h'):
        byte_len = 2


    class uInt2(Int1, key='H'):  # noqa
        byte_len = 2


    class Int4(Int1, key='l'):
        byte_len = 4


    class uInt4(Int1, key='L'):  # noqa
        byte_len = 4


    class Int8(Int1, key='q'):
        byte_len = 8


    class uInt8(Int1, key='Q'):  # noqa
        byte_len = 8


def Size(amount: int = 1) -> Type[int]:  # noqa
    return _Size.mutate(amount)


def uSize(amount: int = 1) -> Type[int]:  # noqa
    return _uSize.mutate(amount)


# endregion

# region Float types

if TYPE_CHECKING:
    Float = Double = Float2 = Float4 = Float8 = float
else:
    class Float2(int, _Type, key='e'):
        @classmethod
        def to_struct_value(cls, v):
            return float(v)

        @classmethod
        def to_python_value(cls, v):
            return float(v)


    class Float(int, _Type, key='f'):
        @classmethod
        def to_struct_value(cls, v):
            return float(v)

        @classmethod
        def to_python_value(cls, v):
            return float(v)


    class Double(int, _Type, key='d'):
        @classmethod
        def to_struct_value(cls, v):
            return float(v)

        @classmethod
        def to_python_value(cls, v):
            return float(v)


    Float4 = Float
    Float8 = Double

# endregion

# region String types

if TYPE_CHECKING:
    _String = _PascalString = str

else:
    class _String(str, DynamicLength, _Type, key='s'):
        strip_null: bool

        @classmethod
        def to_struct_value(cls, v):
            if len(v) > cls.amount:
                raise ValueError(f'Max length exceeded: {len(v)}/{cls.amount}')
            if isinstance(v, str):
                return v.encode(ENCODING)
            return bytes(v)

        @classmethod
        def to_python_value(cls, v):
            v = bytes(v)
            if cls.strip_null:
                v = v.replace(b'\x00', b'')
            return v.decode(ENCODING)


    class _PascalString(_String, key='p'):
        pass


def String(amount: int = 1, strip_null: bool = True) -> Type[str]:  # noqa
    return _String.mutate(amount, strip_null=strip_null)


def PascalString(amount: int = 1, strip_null: bool = True) -> Type[str]:  # noqa
    return _PascalString.mutate(amount, strip_null=strip_null)
# endregion

# endregion
