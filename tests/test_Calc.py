def test_add():
    x,y = 1,2
    instance = Calculator(x,y)
    assert instance.add() == x + y, "Add method doesn't work!"