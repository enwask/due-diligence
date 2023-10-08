from google.cloud import secretmanager as mgr
from google_crc32c import Checksum

# Constants
__GOOGLE_CLOUD_PROJECT_ID = "knighthacks23"
__OPENAI_KEY_ID = "openai_key"
__GOOGLE_SEARCH_KEY_ID = "google_search_key"
__OXYLABS_USER_ID = "oxylabs_user"
__OXYLABS_KEY_ID = "oxylabs_key"


# Fetch a secret from Google Secret Manager
def __get_secret(secret_id: str, version_id: str = "latest") -> str:
    client = mgr.SecretManagerServiceClient()
    name = f"projects/{__GOOGLE_CLOUD_PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})

    # Verify checksum
    checksum = Checksum()
    checksum.update(response.payload.data)
    if int(checksum.hexdigest(), 16) != response.payload.data_crc32c:
        print("Invalid checksum when retrieving secret")
        return str(response)

    return response.payload.data.decode("UTF-8")


openai_key: str = __get_secret(__OPENAI_KEY_ID)
google_search_key: str = __get_secret(__GOOGLE_SEARCH_KEY_ID)
oxylabs_user: str = __get_secret(__OXYLABS_USER_ID)
oxylabs_key: str = __get_secret(__OXYLABS_KEY_ID)

__all__ = ["openai_key", "google_search_key", "oxylabs_user", "oxylabs_key"]
