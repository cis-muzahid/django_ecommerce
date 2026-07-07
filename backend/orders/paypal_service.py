import requests
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings


class PayPalAPIError(Exception):
    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response


def paypal_configured():
    return bool(settings.PAYPAL_CLIENT_ID and settings.PAYPAL_CLIENT_SECRET)


def paypal_api_base():
    mode = getattr(settings, 'PAYPAL_MODE', 'sandbox')
    if mode == 'live':
        return 'https://api.paypal.com'
    return 'https://api.sandbox.paypal.com'


def paypal_currency():
    """PayPal charge currency. USD works reliably in sandbox; INR needs India live merchant setup."""
    return getattr(settings, 'PAYPAL_CURRENCY', 'USD')


def paypal_inr_to_usd_rate():
    return Decimal(str(getattr(settings, 'PAYPAL_INR_TO_USD_RATE', '83')))


def prepare_paypal_amount(store_amount):
    """
    Store prices are INR. PayPal sandbox typically requires USD.
    Returns (formatted_amount_str, currency_code, display_note).
    """
    currency = paypal_currency()
    amount = Decimal(str(store_amount))

    if currency == 'USD':
        converted = (amount / paypal_inr_to_usd_rate()).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if converted < Decimal('0.01'):
            converted = Decimal('0.01')
        return _format_amount(converted), 'USD', {
            'store_amount': float(amount),
            'store_currency': 'INR',
            'paypal_amount': float(converted),
            'paypal_currency': 'USD',
            'exchange_rate': float(paypal_inr_to_usd_rate()),
        }

    return _format_amount(amount), currency, {
        'store_amount': float(amount),
        'store_currency': 'INR',
        'paypal_amount': float(amount),
        'paypal_currency': currency,
    }


def get_access_token():
    response = requests.post(
        f'{paypal_api_base()}/v1/oauth2/token',
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
        data={'grant_type': 'client_credentials'},
        timeout=30,
    )
    if not response.ok:
        raise PayPalAPIError(_extract_error_message(response), response)
    return response.json()['access_token']


def _auth_headers(access_token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }


def _extract_error_message(response):
    try:
        payload = response.json()
    except ValueError:
        return response.text or 'PayPal request failed'

    details = payload.get('details') or []
    if details:
        detail = details[0]
        return detail.get('description') or detail.get('issue') or payload.get('message', 'PayPal request failed')
    return payload.get('message') or payload.get('name') or 'PayPal request failed'


def _format_amount(amount):
    return f'{float(amount):.2f}'


def create_checkout_order(*, amount, currency, custom_id, return_url, cancel_url, description):
    access_token = get_access_token()
    # Always use en-US for USD sandbox to avoid India locale conflicts on checkout
    locale = 'en-US' if currency == 'USD' else ('en-IN' if currency == 'INR' else 'en-US')
    payload = {
        'intent': 'CAPTURE',
        'application_context': {
            'brand_name': 'Ecommerce Store',
            'locale': locale,
            'landing_page': 'LOGIN',
            'shipping_preference': 'NO_SHIPPING',
            'user_action': 'PAY_NOW',
            'return_url': return_url,
            'cancel_url': cancel_url,
        },
        'purchase_units': [{
            'amount': {
                'currency_code': currency,
                'value': _format_amount(amount),
            },
            'custom_id': str(custom_id or ''),
            'description': description,
        }],
    }

    response = requests.post(
        f'{paypal_api_base()}/v2/checkout/orders',
        headers=_auth_headers(access_token),
        json=payload,
        timeout=30,
    )
    if not response.ok:
        error_message = _extract_error_message(response)
        if currency != 'USD' and 'currency' in error_message.lower():
            store_amount = Decimal(str(amount))
            converted = (store_amount / paypal_inr_to_usd_rate()).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            if converted < Decimal('0.01'):
                converted = Decimal('0.01')
            return create_checkout_order(
                amount=_format_amount(converted),
                currency='USD',
                custom_id=custom_id,
                return_url=return_url,
                cancel_url=cancel_url,
                description=description,
            )
        raise PayPalAPIError(error_message, response)

    data = response.json()
    approval_url = None
    for link in data.get('links', []):
        if link.get('rel') == 'approve':
            approval_url = link.get('href')
            if currency == 'INR' and approval_url and 'locale.x=' not in approval_url:
                separator = '&' if '?' in approval_url else '?'
                approval_url = f'{approval_url}{separator}locale.x=en_IN&country.x=IN'
            break

    return {
        'id': data.get('id'),
        'status': data.get('status'),
        'approval_url': approval_url,
        'currency': currency,
        'amount': _format_amount(amount),
        'raw': data,
    }


def create_checkout_order_from_store_amount(*, store_amount, custom_id, return_url, cancel_url, description):
    paypal_amount, currency, conversion = prepare_paypal_amount(store_amount)
    result = create_checkout_order(
        amount=paypal_amount,
        currency=currency,
        custom_id=custom_id,
        return_url=return_url,
        cancel_url=cancel_url,
        description=description,
    )
    result['conversion'] = conversion
    return result


def capture_checkout_order(paypal_order_id):
    access_token = get_access_token()
    response = requests.post(
        f'{paypal_api_base()}/v2/checkout/orders/{paypal_order_id}/capture',
        headers=_auth_headers(access_token),
        json={},
        timeout=30,
    )
    if not response.ok:
        raise PayPalAPIError(_extract_error_message(response), response)
    return response.json()


def get_checkout_order(paypal_order_id):
    access_token = get_access_token()
    response = requests.get(
        f'{paypal_api_base()}/v2/checkout/orders/{paypal_order_id}',
        headers=_auth_headers(access_token),
        timeout=30,
    )
    if not response.ok:
        raise PayPalAPIError(_extract_error_message(response), response)
    return response.json()


def get_capture_id_from_order(paypal_order_id):
    """
    Retrieve the capture ID from a completed PayPal v2 order.
    The capture ID (not the order ID) is required to issue a refund.
    Returns the first capture ID found, or None.
    """
    order_data = get_checkout_order(paypal_order_id)
    for unit in order_data.get('purchase_units', []):
        for capture in unit.get('payments', {}).get('captures', []):
            capture_id = capture.get('id')
            if capture_id:
                return capture_id
    return None


def refund_capture(capture_id, amount=None, currency=None, note=None):
    """
    Issue a full or partial refund against a PayPal capture.

    Args:
        capture_id: The PayPal capture ID (from purchase_units[].payments.captures[].id).
        amount:     Decimal or float — the refund amount in the PayPal charge currency.
                    Pass None for a full refund.
        currency:   The currency code (e.g. 'USD'). Required if amount is provided.
        note:       Optional note to the buyer visible in their PayPal account.

    Returns:
        dict: PayPal refund response JSON.
    """
    access_token = get_access_token()
    payload = {}
    if amount is not None:
        payload['amount'] = {
            'value': _format_amount(amount),
            'currency_code': currency or paypal_currency(),
        }
    if note:
        payload['note_to_payer'] = note[:255]  # PayPal max 255 chars

    response = requests.post(
        f'{paypal_api_base()}/v2/payments/captures/{capture_id}/refund',
        headers=_auth_headers(access_token),
        json=payload,
        timeout=30,
    )
    if not response.ok:
        raise PayPalAPIError(_extract_error_message(response), response)
    return response.json()
