import re
import base64

from requests import Session
from collections import OrderedDict

# Modified code based on DashLt's spoofbuz

_SEED_TIMEZONE_REGEX = re.compile(
    r'[a-z]\.initialSeed\("(?P<seed>[\w=]+)",window\.utimezone\.(?P<timezone>[a-z]+)\)'
)
_INFO_EXTRAS_REGEX = r'name:"\w+/(?P<timezone>{timezones})",info:"(?P<info>[\w=]+)",extras:"(?P<extras>[\w=]+)"'
_APP_ID_REGEX = re.compile(
    r'{app_id:"(?P<app_id>\d{9})",app_secret:"\w{32}",base_port:"80",base_url:"https://www\.qobuz\.com",base_method:"/api\.json/0\.2/"},n'
)

_BUNDLE_URL_REGEX = re.compile(
    r'<script src="(/resources/\d+\.\d+\.\d+-[a-z]\d{3}/bundle\.js)"></script>'
)

_BASE_URL = "https://play.qobuz.com"
_BUNDLE_URL_REGEX = re.compile(
    r'<script src="(/resources/\d+\.\d+\.\d+-[a-z]\d{3}/bundle\.js)"></script>'
)


class Bundle:
    def __init__(self):
        self._session = Session()

        response = self._session.get(f"{_BASE_URL}/login")
        response.raise_for_status()

        bundle_url_match = _BUNDLE_URL_REGEX.search(response.text)
        if not bundle_url_match:
            raise NotImplementedError("Bundle URL found")

        bundle_url = bundle_url_match.group(1)

        response = self._session.get(_BASE_URL + bundle_url)
        response.raise_for_status()

        self._bundle = response.text

    def get_app_id(self):
        if match := _APP_ID_REGEX.search(self._bundle):
            return match.group("app_id")
        else:
            raise NotImplementedError("Failed to match APP ID")

    def get_secrets(self):
        seed_matches = _SEED_TIMEZONE_REGEX.finditer(self._bundle)
        secrets = OrderedDict()

        for match in seed_matches:
            seed, timezone = match.group("seed", "timezone")
            secrets[timezone] = [seed]

        keypairs = list(secrets.items())
        secrets.move_to_end(keypairs[1][0], last=False)
        info_extras_regex = _INFO_EXTRAS_REGEX.format(
            timezones="|".join([timezone.capitalize() for timezone in secrets])
        )
        info_extras_matches = re.finditer(info_extras_regex, self._bundle)
        for match in info_extras_matches:
            timezone, info, extras = match.group("timezone", "info", "extras")
            secrets[timezone.lower()] += [info, extras]
        for secret_pair in secrets:
            secrets[secret_pair] = base64.standard_b64decode(
                "".join(secrets[secret_pair])[:-44]
            ).decode("utf-8")
        return secrets