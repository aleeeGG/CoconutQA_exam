def assert_movie_fields(data):
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "price" in data
    assert "imageUrl" in data
    assert "location" in data
    assert "published" in data
    assert "rating" in data
    assert "genreId" in data
