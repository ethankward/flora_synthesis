from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_ratelimiter import LimiterSession


def get_session():
    session = LimiterSession(per_second=1)

    session.mount('http://', HTTPAdapter(max_retries=Retry(total=5,
                                                           backoff_factor=2,
                                                           status_forcelist=[429, 500, 502, 503, 504])))
    return session
