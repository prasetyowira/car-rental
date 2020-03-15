def test_example_response_example(client):
    assert client.get("/example/")


def test_example_response_1(client):
    assert client.get("/1")


def test_example_response_2(client):
    assert client.get("/2")
