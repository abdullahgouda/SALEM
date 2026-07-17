import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings


class BrevoEmailError(Exception):
    """Raised when sending email through Brevo API fails."""


def send_transactional_email(*, to_email, subject, text_content, to_name=None):
    api_key = str(getattr(settings, "BREVO_API_KEY", "") or "").strip()
    if not api_key:
        raise BrevoEmailError("BREVO_API_KEY is not configured.")

    sender_email = str(
        getattr(settings, "BREVO_SENDER_EMAIL", "") or getattr(settings, "DEFAULT_FROM_EMAIL", "")
    ).strip()
    if not sender_email:
        raise BrevoEmailError("BREVO_SENDER_EMAIL or DEFAULT_FROM_EMAIL must be configured.")

    sender_name = str(getattr(settings, "BREVO_SENDER_NAME", "Salem BackEnd") or "Salem BackEnd").strip()
    base_url = str(getattr(settings, "BREVO_API_BASE_URL", "https://api.brevo.com/v3")).rstrip("/")
    timeout = int(getattr(settings, "BREVO_EMAIL_TIMEOUT", 30))

    recipient = {"email": to_email}
    if to_name:
        recipient["name"] = to_name

    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [recipient],
        "subject": subject,
        "textContent": text_content,
    }

    request = Request(
        url=f"{base_url}/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key,
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw_body = response.read().decode("utf-8") if response else ""
            if response.status not in (200, 201):
                raise BrevoEmailError(f"Brevo API returned status {response.status}: {raw_body}")
            if not raw_body:
                return {}
            return json.loads(raw_body)
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        raise BrevoEmailError(f"Brevo API HTTP error {exc.code}: {error_body}") from exc
    except URLError as exc:
        raise BrevoEmailError(f"Brevo API connection error: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise BrevoEmailError(f"Brevo API returned invalid JSON response: {exc}") from exc