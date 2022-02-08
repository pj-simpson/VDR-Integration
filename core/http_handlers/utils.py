from django.core.cache import cache

from core.models import RemoteSystemSettings


def get_setting(setting_name):

    """
    simple function which sits as an abstraction over the verbose ORM query to return a
    single value for a given setting.

    previously doing something like this:
        RemoteSystemSettings.objects.only('setting_name').first().setting_name

    We first try and retrieve the setting from the cache before looking in the DB. If we get from the DB, we
    set the cache.

    :param setting_name: string
    :return: the value of the given setting
    """
    single_setting = cache.get(setting_name)

    if single_setting is None:
        setting_object = RemoteSystemSettings.objects.only(setting_name).first()
        single_setting = getattr(setting_object, setting_name)

        cache.set(setting_name, single_setting)

    return single_setting
