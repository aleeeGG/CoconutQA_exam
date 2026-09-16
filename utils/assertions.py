def assert_movie_fields(data):
    assert data.get("id") is not None
    assert data.get("name") is not None
    assert data.get("description") is not None
    assert data.get("price") is not None
    assert data.get("imageUrl") is not None
    assert data.get("location") is not None
    assert data.get("published") is not None
    assert data.get("rating") is not None
    assert data.get("genreId") is not None

