from rest_framework import status

from rest_framework.response import Response

from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from .utils import (
    create_azure_user, update_azure_user,
    delete_azure_user, update_azure_user_password
)


class ResponseInfo(object):
    """
    Class for setting how API should send response.
    """

    def __init__(self, **args):
        self.response = {
            "status_code": args.get('status', 200),
            "error": args.get('error', None),
            "data": args.get('data', []),
            "message": [args.get('message', 'Success')]
        }


class AddUser(CreateAPIView):
    """
    Class for creating api for adding practices.
    """
    permission_classes = ()
    authentication_classes = ()

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(AddUser, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        auth_data = create_azure_user(request.META.get('HTTP_AUTHORIZATION'), request.data, True)
        if auth_data['user_status']:
            self.response_format["data"] = auth_data
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["error"] = None
            self.response_format["message"] = "User added successfully"
            return Response(self.response_format)
        else:
            self.response_format["data"] = None
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["error"] = auth_data['error']
            self.response_format["message"] = "Please check data"
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(UpdateAPIView):
    """
    Class for creating api for adding practices.
    """
    permission_classes = ()
    authentication_classes = ()

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UpdateUser, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        auth_data = update_azure_user(request.META.get('HTTP_AUTHORIZATION'), request.data, True)
        if auth_data['user_status']:
            self.response_format["data"] = auth_data
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["error"] = None
            self.response_format["message"] = "User updated successfully"
            return Response(self.response_format)
        else:
            self.response_format["data"] = None
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["error"] = auth_data['error']
            self.response_format["message"] = "Please check data"
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class DeleteUser(DestroyAPIView):
    """
    Class for creating api for adding practices.
    """
    permission_classes = ()
    authentication_classes = ()

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(DeleteUser, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        auth_data = delete_azure_user(request.META.get('HTTP_AUTHORIZATION'), request.data, True)
        if auth_data['user_status']:
            self.response_format["data"] = auth_data
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["error"] = None
            self.response_format["message"] = "User deleted successfully"
            return Response(self.response_format)
        else:
            self.response_format["data"] = None
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["error"] = auth_data['error']
            self.response_format["message"] = "Please check data"
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserPassword(UpdateAPIView):
    permission_classes = ()
    authentication_classes = ()

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UpdateUserPassword, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        auth_data = update_azure_user_password(request.META.get('HTTP_AUTHORIZATION'), request.data, True)
        if auth_data['user_status']:
            self.response_format["data"] = auth_data
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["error"] = None
            self.response_format["message"] = "User password updated successfully"
            return Response(self.response_format)
        else:
            self.response_format["data"] = None
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["error"] = auth_data['error']
            self.response_format["message"] = "Please check data"
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
