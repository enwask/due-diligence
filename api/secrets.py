from google.cloud import secretmanager as mgr
from google_crc32c import Checksum
from os import getenv as env

# Constants
__GOOGLE_CLOUD_PROJECT_ID = "knighthacks23"
__OPENAI_KEY_ID = "openai_key"
__GOOGLE_SEARCH_KEY_ID = "google_search_key"


# Fetch a secret from Google Secret Manager
def __get_secret(secret_id: str, version_id: str = "latest",
                 enc: str = "UTF-8") -> str | mgr.AccessSecretVersionResponse:
    client = mgr.SecretManagerServiceClient()
    name = f"projects/{__GOOGLE_CLOUD_PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})

    # Verify checksum
    checksum = Checksum()
    checksum.update(response.payload.data)
    if int(checksum.hexdigest(), 16) != response.payload.data_crc32c:
        print("Invalid checksum when retrieving secret")
        return response

    return response.payload.data.decode(enc)


# Fetch the OpenAI key from Google Secret Manager
def __get_secret_openai(version_id: str = "latest"):
    return __get_secret(__OPENAI_KEY_ID, version_id)


# Fetch the Google Search key, from .env (if running locally) or from the Secret Manager
def __get_secret_google_search(version_id: str = "latest"):
    # If running locally, use the key in the .env file
    if env("SERVER_SOFTWARE", "").startswith("Development"):
        print("Using local Google Search key")
        return env("GOOGLE_SEARCH_API_KEY")

    # Otherwise fetch the key from the Secret Manager
    return __get_secret(__GOOGLE_SEARCH_KEY_ID, version_id)


openai_key = __get_secret_openai()
google_search_key = __get_secret_google_search()

__all__ = ["openai_key", "google_search_key"]
