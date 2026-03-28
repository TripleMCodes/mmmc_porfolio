def test_index_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_data(as_text=True)
    # The user's name is uppercased in the template context
    assert "ARTIST NAME" in data


def test_home_alias_renders(client):
    resp = client.get("/Home")
    assert resp.status_code == 200
