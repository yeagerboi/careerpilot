import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

# Strip trailing /rest/v1/ if present - the Supabase client adds this automatically
if url.endswith("/rest/v1/"):
    url = url.replace("/rest/v1/", "")
elif url.endswith("/rest/v1"):
    url = url.replace("/rest/v1", "")

supabase: Client = create_client(url, key)