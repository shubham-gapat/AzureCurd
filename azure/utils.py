import requests
from rest_framework.utils import json
from django.conf import settings

from .permissions import get_access_token


def create_azure_user(token, user_data, is_practice_admin):
    data = {}
    access_token = get_access_token(settings.PHYSICIAN_AUTH0_DOMAIN, settings.PHYSICIAN_AUTH0_AUDIENCE, settings.PHYSICIAN_CLIENT_ID,
                                    settings.PHYSICIAN_CLIENT_SECRET)

    # You can perform additional checks or retrieve user information from the decoded_token if needed.
    if access_token:
        url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/userinfo'
        api_data = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                "Authorization": token},
        )
        if api_data.status_code == 200:
            user_id = api_data.json().get("sub")
            url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/api/v2/users/' + user_id
            azure_token = requests.get(
                url,
                headers={
                    "Authorization": "Bearer " + access_token},
            )
            if azure_token.status_code == 200:
                azure_access_token = azure_token.json().get("identities")[0].get("access_token")
                user = requests.post(
                    settings.AZURE_NEW_USER_URL,
                    data=json.dumps({
                        "accountEnabled": True,
                        "displayName": user_data["first_name"] + " " + user_data["last_name"],
                        "mailNickname": "birth-model-user",
                        "userPrincipalName": user_data['email'],
                        "businessPhones": [str(user_data['country_code']) + " " + str(user_data['phone_no'])],
                        "passwordProfile": {
                            "forceChangePasswordNextSignIn": True,
                            "password": "Test@123"
                        },
                    }),
                    headers={
                        "Authorization": "Bearer " + azure_access_token,
                        'Content-Type': 'application/json'
                    },
                )
                if user.status_code == 200 or user.status_code == 201:
                    if is_practice_admin:
                        user_permission = requests.post(
                            settings.AZURE_PERMISSION_ACCESS_URL,
                            data=json.dumps(
                                {
                                    "@odata.type": settings.AZURE_ROLE_TYPE,
                                    "roleDefinitionId": settings.AZURE_ROLE_ID,
                                    "principalId": user.json().get("id"),
                                    "directoryScopeId": "/"
                                }
                            ),
                            headers={
                                "Authorization": "Bearer " + azure_access_token,
                                'Content-Type': 'application/json'
                            },
                        )
                        permission = user_permission.json()
                        if user_permission.status_code == 200 or user_permission.status_code == 201:
                            data.update({
                                "user_status": True,
                                "user_id": "",
                                "azure_id": user.json().get("id")
                            })
                        else:
                            delete_user = requests.delete(
                                settings.AZURE_NEW_USER_URL + "/" + user.json().get("id"),
                                headers={
                                    "Authorization": "Bearer " + azure_access_token,
                                    'Content-Type': 'application/json'
                                },
                            )
                            data.update({
                                "user_status": False,
                                "user_id": "",
                                "azure_id": "",
                                "error": permission
                            })
                    else:
                        data.update({
                            "user_status": True,
                            "user_id": "",
                            "azure_id": user.json().get("id")
                        })
                else:
                    data.update({
                        "user_status": False,
                        "user_id": "",
                        "azure_id": "",
                        "error": user.json()
                    })
            else:
                data.update({
                    "user_status": False,
                    "user_id": "",
                    "azure_id": "",
                    "error": "Azure access permission issue"
                })
        else:
            data.update({
                "user_status": False,
                "user_id": "",
                "azure_id": "Azure access permission issue",
                "error": ""
            })
    else:
        data.update({
            "user_status": False,
            "user_id": "",
            "azure_id": "",
            "error": "Azure access permission issue"
        })
    return data


def update_azure_user(user_data, token):
    data = {}
    access_token = get_access_token(settings.PHYSICIAN_AUTH0_DOMAIN, settings.PHYSICIAN_AUTH0_AUDIENCE, settings.PHYSICIAN_CLIENT_ID,
                                    settings.PHYSICIAN_CLIENT_SECRET)
    if access_token:
        url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/userinfo'
        api_data = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                "Authorization": token},
        )
        if api_data.status_code == 200:
            user_id = api_data.json().get("sub")
            url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/api/v2/users/' + user_id
            azure_token = requests.get(
                url,
                headers={
                    "Authorization": "Bearer " + access_token},
            )
            if azure_token.status_code == 200:
                azure_access_token = azure_token.json().get("identities")[0].get("access_token")
                user = requests.patch(
                    settings.AZURE_NEW_USER_URL + "/" + user_data.email,
                    data=json.dumps({
                        "accountEnabled": True,
                        "displayName": user_data['first_name'] + " " + user_data['last_name'],
                        "mailNickname": "birth-model-user",
                        "businessPhones": [str(user_data['country_code']) + " " + str(user_data['phone_no'])],
                    }),
                    headers={
                        "Authorization": "Bearer " + azure_access_token,
                        'Content-Type': 'application/json'
                    },
                )
                if user.status_code == 200 or user.status_code == 201 or user.status_code == 204:
                    data.update({
                        "user_status": True,
                        "user_id": user_id,
                    })
        else:
            data.update({
                "user_status": False,
                "user_id": ""
            })
    else:
        data.update({
            "user_status": False,
            "user_id": ""
        })
    return data


def delete_azure_user(token, user_data):
    access_token = get_access_token(settings.PHYSICIAN_AUTH0_DOMAIN, settings.PHYSICIAN_AUTH0_AUDIENCE, settings.PHYSICIAN_CLIENT_ID,
                                    settings.PHYSICIAN_CLIENT_SECRET)

    # You can perform additional checks or retrieve user information from the decoded_token if needed.
    if access_token:
        url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/userinfo'
        api_data = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                "Authorization": token},
        )
        if api_data.status_code == 200:
            user_id = api_data.json().get("sub")
            url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/api/v2/users/' + user_id
            azure_token = requests.get(
                url,
                headers={
                    "Authorization": "Bearer " + access_token},
            )
            if azure_token.status_code == 200:
                azure_access_token = azure_token.json().get("identities")[0].get("access_token")
                delete_user = requests.delete(
                    settings.AZURE_NEW_USER_URL + "/" + user_data['email'],
                    headers={
                        "Authorization": "Bearer " + azure_access_token,
                        'Content-Type': 'application/json'
                    },
                )
                if delete_user.status_code == 200 or delete_user.status_code == 201 or delete_user.status_code == 204:
                    url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/api/v2/users/' + user_data.user_auth0_id
                    api_data = requests.delete(
                        url,
                        headers={
                            'Content-Type': 'application/json',
                            "Authorization": "Bearer" + " " + access_token},
                    )
                    if api_data.status_code == 200 or api_data.status_code == 201 or api_data.status_code == 204:
                        return api_data
                return delete_user


def update_azure_user_password(user_data, token):
    data = {}
    access_token = get_access_token(settings.PHYSICIAN_AUTH0_DOMAIN, settings.PHYSICIAN_AUTH0_AUDIENCE, settings.PHYSICIAN_CLIENT_ID,
                                    settings.PHYSICIAN_CLIENT_SECRET)
    if access_token:
        url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/userinfo'
        api_data = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                "Authorization": token},
        )
        if api_data.status_code == 200:
            user_id = api_data.json().get("sub")
            url = 'https://' + settings.PHYSICIAN_AUTH0_DOMAIN + '/api/v2/users/' + user_id
            azure_token = requests.get(
                url,
                headers={
                    "Authorization": "Bearer " + access_token},
            )
            if azure_token.status_code == 200:
                azure_access_token = azure_token.json().get("identities")[0].get("access_token")
                user = requests.post(
                    settings.AZURE_URL + "/changePassword",
                    data=json.dumps(
                        {
                            "currentPassword": user_data["old_password"],
                            "newPassword": user_data["password"]
                        }
                    ),
                    headers={
                        "Authorization": "Bearer " + azure_access_token,
                        'Content-Type': 'application/json'
                    },
                )
                if user.status_code == 200 or user.status_code == 201 or user.status_code == 204:
                    data.update({
                        "user_status": True,
                        "user_id": user_id,
                        "status_code": 204
                    })
                else:
                    data.update({
                        "user_status": False,
                        "user_id": user_id,
                        "error": user.json(),
                        "status_code": 401
                    })
        else:
            data.update({
                "user_status": False,
                "user_id": "",
                "status_code": 401
            })
    else:
        data.update({
            "user_status": False,
            "user_id": "",
            "status_code": 401
        })
    return data
