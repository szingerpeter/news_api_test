import requests

class NewsApi():
    def __init__(self, api_key, api_version = "v2", session = None):
        self._api_key = api_key
        self._api_version = api_version
        self._endpoint_template = f"https://newsapi.org/{self._api_version}/%(endpoint)s"
        self._request_header = self._get_request_header()
        if session:
            self._session = session
        else:
            self._session = requests.Session()
    def _get_request_header(self):
        return {"Authorization": self._api_key}
    def _check_response(self, resp):
        if resp.status_code == 200:
            return True
        elif resp.status_code == 429:
            raise ValueError("Too many requests")
        else:
            print(resp.status_code, resp.reason, resp.text)
            return None
    def _process_pagination(self, endpoint, params, payload_key, itemcount_key):
        tmp = []
        while True:
            try:
                resp = self._session.get(
                    url = endpoint,
                    headers = self._request_header,
                    params = params
                )
            except Exception as e:
                print(f"Exception {str(e)}")
                break
            if self._check_response(resp):
                resp_json = resp.json()
                tmp += resp_json[payload_key]
                maxItems, page = resp_json[itemcount_key], params.get("page", 1)
                if params.get("pageSize", 20) * page >= maxItems:
                    break
                params["page"] = page + 1
            else:
                break
        return tmp
    def get_sources(self, language = "en"):
        try:
            resp = self._session.get(
                url = self._endpoint_template % {"endpoint": "sources"}, 
                headers = self._request_header,
                params = {"language": language}
            )
        except Exception as e:
            print(f"Exception {str(e)}")
            return
        if self._check_response(resp):
            return resp.json()["sources"]
    def get_top_headlines(self, sources = None):
        params = {"pageSize": 100, "page": 1}
        if sources:
            params["sources"] = sources
        return self._process_pagination(
            self._endpoint_template % {"endpoint": "top-headlines"}, 
            params,
            "articles",
            "totalResults"
        )