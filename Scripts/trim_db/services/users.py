import secrets
from ..schema.users.models import ApiKey
from .generic import GenericService



class UserService(GenericService):
    __model__ = None  # DEFINE IN APP
    __unique_on__ = ['email']

    @classmethod
    def from_key(cls, value):
        k = ApiKeyService.get(value=value)
        if k:
            return k.user
        return None

    def __init__(self, user):
        super().__init__(user)
        self._user = user

    def get_key(self):
        return ApiKeyService.get(user_id=self._user.id)

    def generate_key(self, disable_old=True):
        if disable_old:
            old_k = self.get_key()
            if old_k:
                self.disable_key(old_k)
        k = ApiKeyService.create(
            value=secrets.token_hex(16), active=True,
            no_commit=True
        )
        k.user = self._user
        ApiKeyService.update(k)
        return k

    def disable_key(self, key_or_value):
        if isinstance(key_or_value, ApiKey):
            k = key_or_value
        else:
            k = ApiKeyService.get(
                value=key_or_value, user_id=self._user.id,
                include_inactive=True
            )
        if not k:
            raise TypeError(f'No Key Found with Value "{key_or_value}"!')
        k.active = False
        ApiKeyService.update(k)

    def enable_key(self, key_or_value):
        if isinstance(key_or_value, ApiKey):
            k = key_or_value
        else:
            k = ApiKeyService.get(
                value=key_or_value, user_id=self._user.id,
                include_inactive=True
            )
        if not k:
            raise TypeError(f'No Key Found with Value "{key_or_value}"!')
        k.active = True
        ApiKeyService.update(k)

    def delete_key(self, value):
        k = ApiKeyService.get(
            value=value, user_id=self._user.id, include_inactive=True
        )
        if k:
            ApiKeyService.delete(k)


class ApiKeyService(GenericService):
    __model__ = ApiKey

    @classmethod
    def get(cls, *args, include_inactive=False, **kwargs):
        keys = super().get_all(*args, **kwargs)
        if not include_inactive:
            keys = [x for x in keys if x.active]
        if keys:
            return keys[-1]
        return None
