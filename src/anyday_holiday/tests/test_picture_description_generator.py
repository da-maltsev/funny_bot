import pytest

from anyday_holiday import PictureDescriptorGenerator


@pytest.fixture
def generator() -> PictureDescriptorGenerator:
    return PictureDescriptorGenerator()


def test_generate_success_description(generator):
    description = generator()
    result = description.split(" ")

    assert any([result[0] in word for word in generator.nice_attributes]) is True
    assert any([result[1] in word for word in generator.nice_creatures]) is True
    assert any([result[2] in word for word in generator.nice_actions]) is True
