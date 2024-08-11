import requests


class PushNotificationService:
    def __init__(self, provider, **credentials):
        self.provider = provider
        self.credentials = credentials

    def send_notification(self, device_token, title, body, image=None, actions=None):
        """
        Send a push notification with optional image and actions.
        """
        if self.provider == "fcm":
            return self._send_fcm_notification(
                device_token, title, body, image, actions
            )
        elif self.provider == "apns":
            return self._send_apns_notification(
                device_token, title, body, image, actions
            )
        else:
            raise ValueError("Unsupported push notification provider")

    def _send_fcm_notification(self, device_token, title, body, image, actions):
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": f"key={self.credentials['api_key']}",
            "Content-Type": "application/json",
        }
        payload = {
            "to": device_token,
            "notification": {
                "title": title,
                "body": body,
                "image": image,
            },
            "data": {"actions": actions or []},
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def _send_apns_notification(self, device_token, title, body, image, actions):
        # Placeholder for APNs implementation with rich media support
        return f"APNs notification sent to {device_token} with title: {title} and body: {body}"
