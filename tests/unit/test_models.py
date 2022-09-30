
# Test to ensure a new record can be created from the models imported
def test_new_country(new_country):
    """
    GIVEN a Country model
    WHEN a new Country is created
    THEN check that a new id is generated
    """
    assert new_country.name == 'Fantasia'
    assert new_country.longitude == '123'
    assert new_country.latitude == '456'
    assert type(new_country.id) is int
