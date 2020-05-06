import pytest

from tests.test_users import login


@pytest.mark.cat
@pytest.mark.regression
def test_create_new_cat_authorized(client):
    token = login(client, "maradona", "123mudar", access_token_only=True)
    header = dict(
        Authorization="Bearer " + token
    )

    result = client.post("/cats/", json=dict(
        name="Pipito Jr"
    ), headers=header)

    assert result.status_code == 201


@pytest.mark.cat
@pytest.mark.regression
def test_create_new_cat_unauthorized(client):
    result = client.post("/cats/", json=dict(
        name="Pipito Jr"
    ))
    assert result.status_code == 401


@pytest.mark.cat
@pytest.mark.regression
def test_get_existing_cat(client):
    result = client.get("/cats/1")
    assert result.status_code == 200


@pytest.mark.cat
@pytest.mark.regression
def test_get_nonexistent_cat(client):
    result = client.get("/cats/10000")
    assert result.status_code == 404


@pytest.mark.cat
@pytest.mark.regression
def test_update_cat(client):
    token = login(client, "maradona", "123mudar", access_token_only=True)
    header = dict(
        Authorization="Bearer " + token
    )
    new_cat_name = "Gato Atualizado."
    result = client.put("/cats/1", json=dict(
        name=new_cat_name
    ), headers=header)

    cat_data = result.get_json()
    assert result.status_code == 200 and cat_data.get('name') == new_cat_name


@pytest.mark.cat
@pytest.mark.regression
def test_update_nonexistent_cat(client):
    token = login(client, "maradona", "123mudar", access_token_only=True)
    header = dict(
        Authorization="Bearer " + token
    )
    new_cat_name = "Gato Atualizado."
    result = client.put("/cats/1090909", json=dict(
        name=new_cat_name
    ), headers=header)

    assert result.status_code == 404


@pytest.mark.cat
@pytest.mark.regression
def test_update_cat_unauthorized(client):
    new_cat_name = "Gato Atualizado."
    result = client.put("/cats/1090909", json=dict(
        name=new_cat_name
    ))

    assert result.status_code == 401


@pytest.mark.cat
@pytest.mark.regression
def test_delete_cat_unauthorized(client):
    result = client.delete("/cats/1")
    assert result.status_code == 401


@pytest.mark.cat
@pytest.mark.regression
def test_delete_cat_authorized(client):
    token = login(client, "maradona", "123mudar", access_token_only=True)
    result = client.delete("/cats/1", headers=dict(
        Authorization="Bearer " + token
    ))
    assert result.status_code == 204