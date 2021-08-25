---
icon: key-asterisk
---

# Supported Types

> See: [Format characters](https://docs.python.org/3.9/library/struct.html#format-characters)

## Padding

| #   | Type        | Python type |
| --- | ----------- | ----------- |
| x   | `Padding()` | `None`      |

Simple padding, it will create `N` empty bytes when packing, and void them when reading.

```python
from struct_model import *

class Form(StructModel):
    pad: Padding(10)
```

## Boolean

| #   | Type   | Python type |
| --- | ------ | ----------- |
| ?   | `Bool` | `bool`      |

> The '?' conversion code corresponds to the _Bool type defined by C99. If this type is not available, it is simulated using a char. In standard mode, it is always represented by one byte.

```python
from struct_model import *

class Form(StructModel):
    is_alive: Bool
```

## Integers

| #   | Type      | Byte size | Range                                                   | Python type | Byte Order          |
| --- | --------- | --------- | ------------------------------------------------------- | ----------- | ------------------- |
| n   | `Size()`  | Custom    | ...                                                     | `int`       | default/native only |
| N   | `uSize()` | Custom    | ...                                                     | `int`       | default/native only |
| b   | `Int1`    | 1         | -128 to 127                                             | `int`       |                     |
| B   | `uInt1`   | 1         | 0 to 255                                                | `int`       |                     |
| h   | `Int2`    | 2         | -32,768 to 32,767                                       | `int`       |                     |
| H   | `uInt2`   | 2         | 0 to 65,535                                             | `int`       |                     |
| l   | `Int4`    | 4         | -2,147,483,648 to 2,147,483,647                         | `int`       |                     |
| L   | `uInt4`   | 4         | 0 to 4,294,967,295                                      | `int`       |                     |
| q   | `Int8`    | 8         | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | `int`       |                     |
| Q   | `uInt8`   | 8         | 0 to 18,446,744,073,709,551,615                         | `int`       |                     |

```python
from struct_model import *

class Form(StructModel):
    id: uInt8
```

## Floats

| Type      | Byte size | Python type | Byte Order          |
| --------- | --------- | ----------- | ------------------- |
| `Float2`* | 2         | `float`     | default/native only |
| `Float4`  | 4         | `float`     |                     |
| `Float8`  | 8         | `float`     |                     |

!!!
*Float2 is [`Half-precision floating-point format`](https://en.wikipedia.org/wiki/Half-precision_floating-point_format)
!!!

```python
from struct_model import *

class Form(StructModel):
    pos_x: Float8
    pos_y: Float8
```

## Char

| #   | Type   | Python type |
| --- | ------ | ----------- |
| c   | `Char` | `bytes`     |

One-byte character

```python
from struct_model import *

class Form(StructModel):
    letter: Char
```

## Strings

| #   | Type           | Python type |
| --- | -------------- | ----------- |
| s   | `Bytes`        | `bytes`     |
| p   | `PascalBytes`  | `bytes`     |
| s   | `String`       | `str`       |
| p   | `PascalString` | `str`       |

`String` and `PascalString` accepts `amount: int = 1` - length, `strip_null: bool = True` - remove NULL bytes when
parsing or not.

> The 'p' format character encodes a “Pascal string”, meaning a short variable-length string stored in a fixed number
> of bytes, given by the count. The first byte stored is the length of the string, or 255, whichever is smaller.
> The bytes of the string follow. If the string passed in to pack() is too long (longer than the count minus 1),
> only the leading count-1 bytes of the string are stored. If the string is shorter than count-1, it is padded with
> null bytes so that exactly count bytes in all are used. Note that for unpack(), the 'p' format character consumes
> count bytes, but that the string returned can never contain more than 255 bytes.

```python
from struct_model import *

class Form(StructModel):
    username: String(64)
```