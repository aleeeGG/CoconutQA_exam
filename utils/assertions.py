def assert_non_empty_field(data):
    assert data.get("id") is not None
    assert data.get("name") is not None
    assert data.get("description") is not None
    assert data.get("price") is not None
    assert data.get("imageUrl") is not None
    assert data.get("location") is not None
    assert "published" in data
    assert data.get("rating") is not None
    assert data.get("genreId") is not None

