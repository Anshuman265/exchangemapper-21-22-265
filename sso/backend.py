import base64

import requests
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse

from sso.helpers import check_key_and_get, get_django_setting_or_default

from main.models import UserInfo


class OauthBackend(ModelBackend):
    def __init__(self):
        self.access_token = None
        self.request = None
        self.UserModel = get_user_model()
        self.FIELDS = get_django_setting_or_default("FIELDS", "")
        self.PROFILE_URL = (
            "https://gymkhana.iitb.ac.in/sso/user/api/user/?fields="
            + self.FIELDS  # join fields when passed in authenticate
        )
        self.GRANT_TYPE = "authorization_code"
        self.TOKEN_URL = "https://gymkhana.iitb.ac.in/sso/oauth/token/"

    def authenticate(self, request=None, code=None, **kwargs):
        if code is None:
            print(
                "code must be present in response from SSO server. LDAP login skipped, Passing on to next auth backend"
            )
            return None
        if request is None:
            print("empty request")
            return None
        self.request = request
        data = (
            "code="
            + code
            + "&redirect_uri="
            + settings.REDIRECT_URI
            + "&grant_type="
            + self.GRANT_TYPE
        )

        auth_response = requests.post(
            self.TOKEN_URL,
            data=data,
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    f"{settings.CLIENT_ID}:{settings.CLIENT_SECRET}".encode("utf-8")
                ).decode("utf-8"),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            verify=True,
        )

        if auth_response.status_code != 200:
            return HttpResponse("Something went wrong", status=400)

        if "access_token" not in auth_response.json():
            return HttpResponse("no access_token", status=400)
        else:
            request.session["access_token"] = self.access_token = auth_response.json()[
                "access_token"
            ]

        user = self.setup_user()
        return user

    def get_or_create_user(self, user_info):
        try:
            user = self.UserModel.objects.get(
                **{self.UserModel.USERNAME_FIELD: user_info["username"]}
            )
            return user

        except self.UserModel.DoesNotExist:
            try:
                mappings = {
                    self.UserModel.USERNAME_FIELD: user_info["username"],
                }



                # mappings=None

                # ====== CREDIT SPECIFIC CODE START =========
                
                userinfo_mappings= dict()

                # djando user data
                mappings['username']= user_info.get('username', 'notfound')
                mappings['first_name']= user_info.get('first_name', 'notfound')
                mappings['last_name']= user_info.get('last_name', 'notfound')

                # additional data
                userinfo_mappings['name']= user_info.get('first_name', 'notfound') +" "+ user_info.get('last_name', 'notfound')
                userinfo_mappings['roll_number']= user_info.get('roll_number', 'notfound')
                userinfo_mappings['email_ldap']= user_info.get('email', 'notfound')

                # program data
                userinfo_mappings['department']= user_info['program']['department_name']
                userinfo_mappings['degree']= user_info['program']['degree_name']
                userinfo_mappings['join_year']= user_info['program']['join_year']
                userinfo_mappings['graduation_year']= user_info['program']['graduation_year']


                # creates new
                userinfo_instance= UserInfo.objects.create(**userinfo_mappings)
                user, _ = self.UserModel.objects.get_or_create(**mappings, userinfo= userinfo_instance)
                userinfo_instance.user= user
                userinfo_instance.save()

                # ====== CREDIT SPECIFIC CODE END =========






                if get_django_setting_or_default("AUTH_PROFILE_MODULE", ""):
                    profile = apps.get_model(settings.AUTH_PROFILE_MODULE)
                    if profile is None:
                        raise ValueError(
                            "Unable to load the profile model, check AUTH_PROFILE_MODULE in your project settings"
                        )
                    else:
                        profile_mapping = {}
                        for (
                            custom_user_field,
                            recieved_ldap_object,
                        ) in get_django_setting_or_default("PROFILE_MAPPING", {}).items():
                            profile_mapping[custom_user_field] = check_key_and_get(
                                user_info, recieved_ldap_object
                            )
                        profile.objects.create(user=user, **profile_mapping)
            except:
                return HttpResponse("Kindly Complete Your SSO Profile at https://gymkhana.iitb.ac.in/profiles/user/ and relogin", status=400)

            return user

    def setup_user(self):
        user_info_response = requests.get(
            self.PROFILE_URL,
            headers={"Authorization": "Bearer " + self.access_token},
            verify=True,
        )
        user_info = user_info_response.json()
        return self.get_or_create_user(user_info)
