# This OAuth is literally so broken it's not funny

from authlib.integrations.requests_client import OAuth2Session


class OAuthService:
    def __init__(self, provider, client_id, client_secret, redirect_uri):
        self.provider = provider
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        if provider == "google":
            self.authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
            self.token_url = "https://accounts.google.com/o/oauth2/token"
            self.scope = ["https://www.googleapis.com/auth/userinfo.email"]
        elif provider == "github":
            self.authorization_base_url = "https://github.com/login/oauth/authorize"
            self.token_url = "https://github.com/login/oauth/access_token"
            self.scope = ["user:email"]
        elif provider == "facebook":
            self.authorization_base_url = "https://www.facebook.com/v8.0/dialog/oauth"
            self.token_url = "https://graph.facebook.com/v8.0/oauth/access_token"
            self.scope = ["email"]
        else:
            raise ValueError("Unsupported OAuth provider")

    def get_authorization_url(self):
        """
        Get the authorization URL to redirect the user to.
        """
        oauth = OAuth2Session(
            client_id=self.client_id, redirect_uri=self.redirect_uri, scope=self.scope
        )
        authorization_url, state = oauth.create_authorization_url(
            self.authorization_base_url
        )
        return authorization_url, state

    def fetch_token(self, authorization_response):
        """
        Fetch the OAuth token after user authorization.
        """
        oauth = OAuth2Session(client_id=self.client_id, redirect_uri=self.redirect_uri)
        token = oauth.fetch_token(
            self.token_url,
            authorization_response=authorization_response,
            client_secret=self.client_secret,
        )
        return token

    def refresh_token(self, refresh_token):
        """
        Refresh an OAuth token.
        """
        oauth = OAuth2Session(
            client_id=self.client_id, token={"refresh_token": refresh_token}
        )
        new_token = oauth.refresh_token(
            self.token_url,
            refresh_token=refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        return new_token
