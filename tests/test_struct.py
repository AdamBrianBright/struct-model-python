import struct_model


class Form(struct_model.StructModel):
    username: struct_model.String(16)
    gold_coins: struct_model.uInt4
    last_seen: struct_model.Double


FORM_BYTES = b'Adam Bright\x00\x00\x00\x00\x00\x00\x00\x00\x14A\x9dZ\xd6\xcc\x00\x00\x00'
FORM_DICT = {'username': 'Adam Bright', 'gold_coins': 20, 'last_seen': 123123123.000}


def test_pack():
    assert Form.from_dict(FORM_DICT).pack() == FORM_BYTES


def test_unpack():
    assert Form.load(FORM_BYTES).dict() == FORM_DICT
