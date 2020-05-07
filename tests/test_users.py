import pytest


def login(client, username, password, access_token_only=False):
    result = client.post("users/login", json=dict(
        username=username, password=password
    ), follow_redirects=True)

    if access_token_only:
        return result.get_json().get('access_token')

    return result


@pytest.mark.user
@pytest.mark.regression
@pytest.mark.skip
def test_list_empty_users(client):
    res = client.get('/users/', follow_redirects=True)
    assert res.status_code == 200 and len(res.get_json()) == 0


@pytest.mark.user
@pytest.mark.regression
def test_create_new_user(client, user_data):
    res = client.post('users/', json=user_data, follow_redirects=True)
    creation_response = res.get_json()
    assert res.status_code == 201 and creation_response.get('id')


@pytest.mark.user
@pytest.mark.regression
def test_user_not_found(client):
    res = login(client, "pipito", "123mudar")
    assert res.status_code == 404


@pytest.mark.user
@pytest.mark.regression
def test_user_invalid_credentials(client):
    res = login(client, "maradona", "123aaaddd")
    assert res.status_code == 403


@pytest.mark.user
@pytest.mark.regression
def test_user_valid_credentials(client, user_data):
    res = login(client, **user_data)
    token_data = res.get_json()
    assert (res.status_code == 200 and 'access_token' in token_data
            and 'refresh_token' in token_data)
