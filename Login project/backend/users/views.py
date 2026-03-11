import base64
import hashlib
import hmac
import json
from datetime import timedelta
from uuid import UUID, uuid4

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


STATIC_USER_ID = "4e4dd113-1c54-49b8-90b9-513a8eaffffd"


def _base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _resolve_user_id(user):
    user_id = str(user.pk)
    try:
        UUID(user_id)
        return user_id
    except (ValueError, TypeError):
        return STATIC_USER_ID


def _encode_jwt(payload):
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = _base64url_encode(
        json.dumps(header, separators=(",", ":")).encode("utf-8")
    )
    encoded_payload = _base64url_encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    unsigned_token = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        unsigned_token.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return f"{unsigned_token}.{_base64url_encode(signature)}"


def _build_user_response(user):
    role = getattr(user, "role", None) or "admin"
    company = getattr(user, "company", None)
    company_id = getattr(user, "company_id", None)
    company_name = getattr(company, "name", None) or getattr(user, "company_name", None) or "JMS Advisory Services Pvt Ltd"
    name = getattr(user, "name", None) or user.get_full_name().strip() or user.get_username()

    role_display = "Admin"
    if role:
        role_display_getter = getattr(user, "get_role_display", None)
        role_display = role_display_getter() if callable(role_display_getter) else role.replace("_", " ").title()

    return {
        "id": _resolve_user_id(user),
        "name": name,
        "email": user.email,
        "role": role,
        "role_display": role_display,
        "company_id": str(company_id) if company_id else "619fdc4b-1a67-4547-96d1-4dcbdf2a4f10",
        "company_name": company_name,
    }


def _build_token_payload(user, token_type, expires_in):
    issued_at = timezone.now()
    expires_at = issued_at + expires_in
    user_data = _build_user_response(user)
    payload = {
        "token_type": token_type,
        "exp": int(expires_at.timestamp()),
        "iat": int(issued_at.timestamp()),
        "jti": uuid4().hex,
        "user_id": _resolve_user_id(user),
        "name": user_data["name"],
    }
    if user_data["role"]:
        payload["role"] = user_data["role"]
    if user_data["company_id"]:
        payload["company_id"] = user_data["company_id"]
    return payload


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are allowed."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON payload."}, status=400)

    email = payload.get("email", "").strip()
    password = payload.get("password", "")

    if not email or not password:
        return JsonResponse({"message": "Email and password are required."}, status=400)

    user_model = get_user_model()
    matching_users = user_model.objects.filter(email__iexact=email)

    authenticated_user = next(
        (
            user
            for user in matching_users
            if user.is_active and user.check_password(password)
        ),
        None,
    )

    if authenticated_user is None:
        return JsonResponse({"message": "Invalid email or password."}, status=401)

    login(request, authenticated_user)
    user_data = _build_user_response(authenticated_user)
    refresh_token = _encode_jwt(
        _build_token_payload(
            authenticated_user,
            token_type="refresh",
            expires_in=timedelta(days=7),
        )
    )
    access_token = _encode_jwt(
        _build_token_payload(
            authenticated_user,
            token_type="access",
            expires_in=timedelta(minutes=15),
        )
    )

    return JsonResponse(
        {
            "message": "Login successful",
            "user": user_data,
            "refresh": refresh_token,
            "access": access_token,
        },
        status=200,
    )
