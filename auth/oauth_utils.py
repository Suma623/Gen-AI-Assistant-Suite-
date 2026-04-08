import httpx
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

def get_google_auth_url():
    if not (GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI):
        return None
    scope = "openid email profile"
    auth_url = (f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code"
                f"&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}"
                f"&scope={scope}&access_type=offline&prompt=consent")
    return auth_url

def exchange_code_for_user_info(code):
    """Exchanges the authorization code for an access token, then fetches user info."""
    if not (GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and GOOGLE_REDIRECT_URI):
        return None, "Google OAuth environment variables are missing."

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_super_secret" : "REPLACED", # Just to prevent accidental bad keys, we will use correct below
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    try:
        # Step 1: Exchange code for Access Token
        token_response = httpx.post(GOOGLE_TOKEN_URL, data=data)
        token_response.raise_for_status()
        token_json = token_response.json()
        access_token = token_json.get("access_token")
        
        if not access_token:
            return None, "Failed to retrieve access token from Google."
            
        # Step 2: Extract User Info combining with the Access Token
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = httpx.get(GOOGLE_USERINFO_URL, headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
        
        return user_info, None
        
    except httpx.HTTPStatusError as e:
        return None, f"HTTP Error during OAuth: {e.response.text}"
    except Exception as e:
        return None, f"An Error occurred: {str(e)}"
