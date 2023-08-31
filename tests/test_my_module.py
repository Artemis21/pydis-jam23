import pytest


@pytest.mark.parametrize(
    ("a", "b", "out"),
    [
        (3, 6, 9),
        (1, 2, 3),
        (17, 12, 29),
    ],
)
def test_add(a, b, out):
    assert a + b == out


def test_smth():
    assert True
