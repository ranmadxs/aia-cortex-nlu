# test_capitalize.py

#poetry run pytest -s

def test_dummy_nlu():
    string = "Dummy"
    print("Example dummy nlu")
    assert string.capitalize() == 'Dummy'


def test_base_nlu():
    print("Test base nlu")
    
    assert True