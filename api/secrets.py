from google.cloud import secretmanager as mgr
from google_crc32c import Checksum

# Constants
PROJECT_ID = "knighthacks23"
OPENAI_KEY_ID = "openai_key"


# Fetch a secret from Google Secret Manager
def get_secret(secret_id: str, version_id: str = "latest", enc: str = "UTF-8") -> str | mgr.AccessSecretVersionResponse:
    client = mgr.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})

    # Verify checksum
    checksum = Checksum()
    checksum.update(response.payload.data)
    if int(checksum.hexdigest(), 16) != response.payload.data_crc32c:
        print("Invalid checksum when retrieving secret")
        return response

    return response.payload.data.decode(enc)


# Fetch the OpenAI key from Google Secret Manager
def get_secret_openai(version_id: str = "latest"):
    return get_secret(OPENAI_KEY_ID, version_id)
