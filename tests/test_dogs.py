import pytest

from tests.test_users import login


def get_one_dog(client):
    cats = client.get("/dogs/").get_json()
    if len(cats) > 0:
        return cats[0]
    return None


@pytest.mark.dog
@pytest.mark.regression
def test_create_new_dog_authorized(client, user_data):
    token = login(client, access_token_only=True, **user_data)
    header = dict(
        Authorization="Bearer " + token
    )

    result = client.post("/dogs/", json=dict(
        name="Lord Jr"
    ), headers=header)

    assert result.status_code == 201


@pytest.mark.dog
@pytest.mark.regression
def test_create_new_dog_unauthorized(client):
    result = client.post("/dogs/", json=dict(
        name="Pipito Jr"
    ))
    assert result.status_code == 401


@pytest.mark.dog
@pytest.mark.regression
def test_get_existing_dog(client):
    result = client.get(f"/dogs/{get_one_dog(client).get('id')}")
    assert result.status_code == 200


@pytest.mark.dog
@pytest.mark.regression
def test_get_nonexistent_cat(client):
    result = client.get("/dogs/111233")
    assert result.status_code == 404


@pytest.mark.dog
@pytest.mark.regression
def test_update_dog(client, user_data):
    token = login(client, access_token_only=True, **user_data)
    header = dict(
        Authorization="Bearer " + token
    )
    new_dog_name = "Mr Dog"
    result = client.put(f"/dogs/{get_one_dog(client).get('id')}", json=dict(
            name=new_dog_name
        ), headers=header)

    dog_data = result.get_json()

    assert result.status_code == 200 and dog_data.get('name') == new_dog_name


@pytest.mark.dog
@pytest.mark.regression
def test_update_nonexistent_dog(client, user_data):
    token = login(client, access_token_only=True, **user_data)
    header = dict(
        Authorization="Bearer " + token
    )
    new_dog_name = "Mr dogdog"
    result = client.put("/dogs/12313123", json=dict(
        name=new_dog_name
    ), headers=header)
    assert result.status_code == 404


@pytest.mark.dog
@pytest.mark.regression
def test_update_dog_unauthorized(client):
    new_dog_name = "Dog Dog"
    result = client.put(f"/dogs/{get_one_dog(client).get('id')}", json=dict(
        name=new_dog_name
    ))
    assert result.status_code == 401


@pytest.mark.dog
@pytest.mark.regression
def test_delete_cat_unauthorized(client):
    result = client.delete("/dogs/11223344")
    assert result.status_code == 401


@pytest.mark.dog
@pytest.mark.regression
def test_delete_cat_authorized(client, user_data):
    token = login(client, access_token_only=True, **user_data)
    result = client.delete(f"/dogs/{get_one_dog(client).get('id')}", headers=dict(
        Authorization="Bearer " + token
    ))
    assert result.status_code == 204