import requests
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter


USER_FIELDS = [
    "first_name",
    "last_name",
    "nickname",
    "screen_name",
    "sex",
    "bdate",
    "city",
    "country",
    "timezone",
    "photo",
    "photo_medium",
    "photo_big",
    "photo_max_orig",
    "has_mobile",
    "contacts",
    "education",
    "online",
    "counters",
    "relation",
    "last_seen",
    "activity",
    "universities",
]


class CustomVKOAuth2Adapter(VKOAuth2Adapter):

    def complete_login(self, request, app, token, **kwargs):
        uid = kwargs['response']['user_id']
        resp = requests.get(self.profile_url,
                            params={'fields': ','.join(USER_FIELDS),
                                    'user_ids': uid})
        resp.raise_for_status()
        extra_data = resp.json()['response'][0]
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)
