# Welcome

## Struct-Model

Struct-Model is an annotations based wrapper for python's built-in `Struct` module.

```python example.py
from struct_model import StructModel, String, uInt4

class Form(StructModel):
    username: String(16)
    balance: uInt4
    
print(Form("Adam Bright", 12).pack())
# b'Adam Bright\x00\x00\x00\x00\x00\x00\x00\x00\x0c'
print(Form.unpack(b'Adam Bright\x00\x00\x00\x00\x00\x00\x00\x00\x0c').json())
# {"username": "Adam Bright", "balance": 12}
```

## Installation

### Poetry

```shell
poetry add struct-model-python
```

### PIP

```shell
pip install struct-model-python
```

## Requirements

+ [`ujson >= 4.1.0`](https://github.com/ultrajson/ultrajson)