import pytest

from src.day16.day16 import Bits, Packet, hex_char_to_bin, hex_to_bin


@pytest.mark.parametrize(
    "hex, want",
    [
        ("0", "0000"),
        ("1", "0001"),
        ("2", "0010"),
        ("3", "0011"),
        ("4", "0100"),
        ("5", "0101"),
        ("6", "0110"),
        ("7", "0111"),
        ("8", "1000"),
        ("9", "1001"),
        ("A", "1010"),
        ("B", "1011"),
        ("C", "1100"),
        ("D", "1101"),
        ("E", "1110"),
        ("F", "1111"),
    ],
)
def test_hex_char_to_bin(hex: str, want: str):
    assert hex_char_to_bin(hex) == want


def test_parse_literal():
    bits = Bits(hex_to_bin("D2FE28"))
    p = Packet.parse(bits)

    # Literal
    assert p.type_id == 4
    assert p.value == 2021
    assert len(p.subpackets) == 0


def test_parse_operator():
    bits = Bits(hex_to_bin("38006F45291200"))
    p = Packet.parse(bits)

    assert p.type_id != 4
    assert p.value is None
    assert len(p.subpackets) == 2


def test_parse_operator_length_type_0():
    bits = Bits(hex_to_bin("EE00D40C823060"))
    p = Packet.parse(bits)

    assert p.type_id != 4
    assert p.value is None
    assert len(p.subpackets) == 3


@pytest.mark.parametrize(
    "hex, want",
    [
        ("8A004A801A8002F478", 16),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_sumversion(hex: str, want: int):
    bits = Bits(hex_char_to_bin(hex))
    p = Packet.parse(bits)

    assert p.sumversion() == want


@pytest.mark.parametrize(
    "hex, want",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_eval_operator_packets(hex: str, want: int):
    bits = Bits(hex_to_bin(hex))
    p = Packet.parse(bits)

    assert p.eval() == want
