import base64
import hashlib
import hmac
import json
import logging
import os
import time
import urllib.parse
import urllib.request
import resend
from datetime import datetime

from flask import Flask, request, jsonify

from sip_client import RawSipRegisterClient


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def _cors(response, origin="*"):
    """Demo request endpoint için CORS header'larını ekler."""
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

BUSINESS_ID = "908505324556"

# ─── Resend Konfigürasyonu ────────────────────────────────────────────────────
# Railway → Variables:
#   RESEND_API_KEY   re_xxxxxxxxxxxx
#   NOTIFY_EMAIL     info@bdlabs.com.tr   (isteğe bağlı, default zaten bu)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
NOTIFY_EMAIL   = os.environ.get("NOTIFY_EMAIL",   "info@bdlabs.com.tr")

# ─── PayTR Konfigürasyonu ─────────────────────────────────────────────────────
# Railway → Variables:
#   PAYTR_MERCHANT_ID    xxxxxxx
#   PAYTR_MERCHANT_KEY   xxxxxxxx...
#   PAYTR_MERCHANT_SALT  xxxxxxxx...

PAYTR_MERCHANT_ID   = os.environ.get("PAYTR_MERCHANT_ID",   "")
PAYTR_MERCHANT_KEY  = os.environ.get("PAYTR_MERCHANT_KEY",  "")
PAYTR_MERCHANT_SALT = os.environ.get("PAYTR_MERCHANT_SALT", "")

# Paket fiyatları (kuruş cinsinden — 999 TL = 99900)
PACKAGE_PRICES = {
    "Temel Paket": 99900,
    "Pro Paket":   199900,
}

# ─── SIP ──────────────────────────────────────────────────────────────────────
_sip = None

def get_sip():
    global _sip
    if _sip is None:
        _sip = RawSipRegisterClient()
    return _sip


# ─── Yardımcı: Tarih normalize ────────────────────────────────────────────────
def normalize_date(date_str):
    """DD-MM-YYYY veya YYYY-MM-DD formatını YYYY-MM-DD'ye çevirir."""
    date_str = date_str.strip()
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Geçersiz tarih formatı: {date_str}")


# ─── Yardımcı: E-posta gönder (Resend HTTP API) ───────────────────────────────
def send_demo_email(data: dict) -> None:
    """
    Demo talep formunu Resend API üzerinden info@bdlabs.com.tr adresine gönderir.
    RESEND_API_KEY eksikse sadece loglar, hata fırlatmaz.
    """
    if not RESEND_API_KEY:
        app.logger.warning("RESEND_API_KEY eksik — e-posta gönderilmedi.")
        app.logger.info("Demo talebi (mail yok): %s", data)
        return

    app.logger.info("Resend API key prefix: %s...", RESEND_API_KEY[:8])

    subject = f"[Ece AI] Yeni Demo Talebi — {data.get('company', 'Bilinmiyor')}"

    html_body = f"""<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#07070f;font-family:Inter,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#07070f;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#0d0d1c;border-radius:16px;border:1px solid #3b1f6e;overflow:hidden;">
        <tr><td style="height:3px;background:linear-gradient(90deg,#7c3aed,#a78bfa);"></td></tr>
        <tr><td style="padding:32px 36px 20px;">
          <p style="margin:0 0 6px;font-size:11px;font-weight:700;color:#a78bfa;letter-spacing:.08em;text-transform:uppercase;">BD Labs · Ece AI</p>
          <h1 style="margin:0;font-size:22px;font-weight:900;color:#f0f0ff;">Yeni Demo Talebi</h1>
          <p style="margin:6px 0 0;font-size:13px;color:#9898b8;">{datetime.now().strftime("%d %B %Y, %H:%M")}</p>
        </td></tr>
        <tr><td style="height:1px;background:#1e1e3a;"></td></tr>
        <tr><td style="padding:24px 36px;">
          <table width="100%" cellpadding="0" cellspacing="0">
            {_email_row("🏢", "Firma Adı", data.get("company",  "—"))}
            {_email_row("👤", "Yetkili",   data.get("contact",  "—"))}
            {_email_row("📞", "Telefon",   data.get("phone",    "—"))}
            {_email_row("✉️", "E-posta",   data.get("email",    "—"))}
            {_email_row("📦", "Paket",     data.get("package",  "Belirtilmedi"))}
            {_email_row("💬", "Not",       data.get("note", "") or "—")}
          </table>
        </td></tr>
        <tr><td style="padding:0 36px 28px;">
          <p style="margin:0;font-size:12px;color:#44445a;line-height:1.6;">
            Bu e-posta <strong style="color:#9898b8;">bdlabs.com.tr</strong> demo talep formu aracılığıyla otomatik oluşturulmuştur.
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    text_body = (
        f"YENİ DEMO TALEBİ — {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"Firma   : {data.get('company',  '—')}\n"
        f"Yetkili : {data.get('contact',  '—')}\n"
        f"Telefon : {data.get('phone',    '—')}\n"
        f"E-posta : {data.get('email',    '—')}\n"
        f"Paket   : {data.get('package',  'Belirtilmedi')}\n"
        f"Not     : {data.get('note', '') or '—'}\n"
    )

    resend.api_key = RESEND_API_KEY

    params: resend.Emails.SendParams = {
        "from":     "BD Labs Ece AI <onboarding@resend.dev>",
        "to":       [NOTIFY_EMAIL],
        "reply_to": data.get("email", NOTIFY_EMAIL),
        "subject":  subject,
        "html":     html_body,
        "text":     text_body,
    }

    result = resend.Emails.send(params)
    app.logger.info("Resend e-posta gönderildi → id=%s", result.get("id"))


def send_payment_email(data: dict) -> None:
    """Başarılı ödeme bildirimini info@bdlabs.com.tr'ye gönderir."""
    if not RESEND_API_KEY:
        app.logger.warning("RESEND_API_KEY eksik — ödeme maili gönderilemedi.")
        return

    subject = f"[Ece AI] ✅ Ödeme Alındı — {data.get('package', '?')} | {data.get('merchant_oid', '')}"

    html_body = f"""<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#07070f;font-family:Inter,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#07070f;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#0d0d1c;border-radius:16px;border:1px solid #14532d;overflow:hidden;">
        <tr><td style="height:3px;background:linear-gradient(90deg,#16a34a,#4ade80);"></td></tr>
        <tr><td style="padding:32px 36px 20px;">
          <p style="margin:0 0 6px;font-size:11px;font-weight:700;color:#4ade80;letter-spacing:.08em;text-transform:uppercase;">BD Labs · Ece AI</p>
          <h1 style="margin:0;font-size:22px;font-weight:900;color:#f0f0ff;">✅ Ödeme Alındı</h1>
          <p style="margin:6px 0 0;font-size:13px;color:#9898b8;">{datetime.now().strftime("%d %B %Y, %H:%M")}</p>
        </td></tr>
        <tr><td style="height:1px;background:#1e1e3a;"></td></tr>
        <tr><td style="padding:24px 36px;">
          <table width="100%" cellpadding="0" cellspacing="0">
            {_email_row("📦", "Paket",       data.get("package",      "—"))}
            {_email_row("💰", "Tutar",       data.get("amount_str",   "—"))}
            {_email_row("🔖", "Sipariş No",  data.get("merchant_oid", "—"))}
            {_email_row("✉️", "E-posta",     data.get("email",        "—"))}
          </table>
        </td></tr>
        <tr><td style="padding:0 36px 28px;">
          <p style="margin:0;font-size:12px;color:#44445a;line-height:1.6;">
            Bu bildirim <strong style="color:#9898b8;">PayTR</strong> ödeme altyapısı tarafından otomatik oluşturulmuştur.
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    text_body = (
        f"ÖDEME ALINDI — {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"Paket      : {data.get('package',      '—')}\n"
        f"Tutar      : {data.get('amount_str',   '—')}\n"
        f"Sipariş No : {data.get('merchant_oid', '—')}\n"
        f"E-posta    : {data.get('email',        '—')}\n"
    )

    resend.api_key = RESEND_API_KEY
    params: resend.Emails.SendParams = {
        "from":    "BD Labs Ece AI <onboarding@resend.dev>",
        "to":      [NOTIFY_EMAIL],
        "subject": subject,
        "html":    html_body,
        "text":    text_body,
    }
    result = resend.Emails.send(params)
    app.logger.info("Ödeme maili gönderildi → id=%s", result.get("id"))
    """E-posta tablosu için tek bir bilgi satırı döner."""
    return f"""
    <tr>
      <td style="padding:8px 0;vertical-align:top;width:28px;font-size:16px;">{icon}</td>
      <td style="padding:8px 12px 8px 0;vertical-align:top;width:110px;
                 font-size:11px;font-weight:700;color:#9898b8;
                 text-transform:uppercase;letter-spacing:.06em;">{label}</td>
      <td style="padding:8px 0;vertical-align:top;
                 font-size:14px;font-weight:600;color:#f0f0ff;">{value}</td>
    </tr>"""


# ─── ENDPOINT'LER ─────────────────────────────────────────────────────────────

@app.post("/incoming")
def incoming():
    app.logger.info("Incoming request body: %s", request.get_data(as_text=True))
    return "", 200


@app.get("/get_slots")
def get_slots():
    """
    ElevenLabs webhook: müsait slotları döner.
    Query param: date (YYYY-MM-DD veya DD-MM-YYYY)
    """
    date = request.args.get("date", "").strip()
    if not date:
        return jsonify({"error": "date parametresi gerekli (DD-MM-YYYY)"}), 400

    try:
        date = normalize_date(date)
        slots = get_sip().get_available_slots(BUSINESS_ID, date)
        return jsonify({
            "date": date,
            "available_slots": slots,
            "count": len(slots)
        })
    except Exception as e:
        app.logger.exception("get_slots error")
        return jsonify({"error": str(e)}), 500


@app.post("/book_appointment")
def book_appointment():
    """
    ElevenLabs webhook: randevu oluşturur.
    JSON body: date, time, name, service (optional), caller_number (optional)
    """
    data = request.get_json(force=True, silent=True) or {}

    date         = data.get("date",          "").strip()
    time_value   = data.get("time",          "").strip()
    name         = data.get("name",          "").strip()
    service      = data.get("service",       "").strip()
    caller_number = data.get("caller_number", "unknown").strip()
    call_id      = data.get("call_id",       f"elevenlabs-{date}-{time_value}").strip()
    transcript   = data.get("transcript",    "").strip()

    if not date or not time_value or not name:
        return jsonify({"error": "date, time ve name zorunlu"}), 400

    try:
        date = normalize_date(date)
        booked = get_sip().book_slot(
            business_id=BUSINESS_ID,
            date=date,
            time_value=time_value,
            caller_number=caller_number,
            name=name,
            call_id=call_id,
            transcript=transcript,
            service=service,
        )
        if booked:
            return jsonify({
                "success": True,
                "message": f"{name} adına {date} tarihinde saat {time_value} için randevu oluşturuldu."
            })
        else:
            return jsonify({
                "success": False,
                "message": f"{date} tarihinde saat {time_value} müsait değil, lütfen başka bir saat seçin."
            }), 409
    except Exception as e:
        app.logger.exception("book_appointment error")
        return jsonify({"error": str(e)}), 500


@app.route("/api/demo-request", methods=["POST", "OPTIONS"])
def demo_request():
    """
    Web sitesi demo talep formu.
    JSON body: company, contact, phone, email, package (optional), note (optional)
    """
    # Tarayıcı preflight isteği — sadece header'larla yanıt ver
    if request.method == "OPTIONS":
        return _cors(app.make_response(("", 204)))

    data = request.get_json(force=True, silent=True) or {}

    company = data.get("company", "").strip()
    contact = data.get("contact", "").strip()
    phone   = data.get("phone",   "").strip()
    email   = data.get("email",   "").strip()
    package = data.get("package", "").strip()
    note    = data.get("note",    "").strip()

    # ── Sunucu tarafı validasyon ───────────────────────────────────────────────
    errors = {}
    if not company:
        errors["company"] = "Firma adı zorunlu"
    if not contact:
        errors["contact"] = "Yetkili adı zorunlu"
    if not phone or len(phone.replace(" ", "").replace("-", "")) < 10:
        errors["phone"] = "Geçerli bir telefon numarası girin"
    if not email or "@" not in email:
        errors["email"] = "Geçerli bir e-posta adresi girin"

    if errors:
        return _cors(jsonify({"success": False, "errors": errors})), 422

    # ── E-posta gönder ────────────────────────────────────────────────────────
    payload = {
        "company": company,
        "contact": contact,
        "phone":   phone,
        "email":   email,
        "package": package or "Belirtilmedi",
        "note":    note,
    }

    try:
        send_demo_email(payload)
    except Exception as e:
        # Mail gönderilemese bile kullanıcıya hata gösterme — sadece logla
        app.logger.exception("Demo e-postası gönderilemedi: %s", e)

    app.logger.info(
        "Demo talebi alındı | firma=%s | yetkili=%s | tel=%s | email=%s | paket=%s",
        company, contact, phone, email, package
    )

    return _cors(jsonify({
        "success": True,
        "message": "Demo talebiniz alındı. Ekibimiz kısa süre içinde sizinle iletişime geçecektir."
    })), 201


@app.route("/api/paytr-token", methods=["POST", "OPTIONS"])
def paytr_token():
    """
    Ödeme başlatma: müşteri bilgilerini alır, PayTR'den iFrame token'ı üretir.
    JSON body: company, contact, phone, email, package, price
    """
    if request.method == "OPTIONS":
        return _cors(app.make_response(("", 204)))

    data = request.get_json(force=True, silent=True) or {}

    email   = data.get("email",   "").strip()
    contact = data.get("contact", "").strip()
    phone   = data.get("phone",   "").strip()
    package = data.get("package", "Temel Paket").strip()
    address = data.get("address", "Türkiye").strip() or "Türkiye"

    if not email or not contact or not phone:
        return _cors(jsonify({"error": "email, contact ve phone zorunlu"})), 422

    # Fiyatı kuruş cinsinden al
    amount = PACKAGE_PRICES.get(package, 99900)

    # Sipariş numarası — benzersiz
    merchant_oid = f"ECE{int(time.time())}"

    # Müşteri IP
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if "," in user_ip:
        user_ip = user_ip.split(",")[0].strip()

    # Sepet (PayTR formatı: JSON array)
    basket = json.dumps([[package, str(amount), 1]])

    # PayTR'nin istediği alanlar
    params = {
        "merchant_id":    PAYTR_MERCHANT_ID,
        "user_ip":        user_ip,
        "merchant_oid":   merchant_oid,
        "email":          email,
        "payment_amount": str(amount),
        "currency":       "TL",
        "payment_type":   "card",
        "installment_count": "0",
        "no_installment": "0",
        "max_installment": "0",
        "user_basket":    basket,
        "debug_on":       "1",           # canlıya geçince "0" yap
        "test_mode":      "1",           # canlıya geçince "0" yap
        "user_name":      contact,
        "user_phone":     phone,
        "user_address":   address,
        "user_city":      "İstanbul",
        "merchant_ok_url":   "https://bdlabs.com.tr",
        "merchant_fail_url": "https://bdlabs.com.tr",
        "timeout_limit":  "30",
        "lang":           "tr",
    }

    # HMAC hash hesapla
    hash_str = (
        PAYTR_MERCHANT_ID +
        user_ip +
        merchant_oid +
        email +
        str(amount) +
        basket +
        params["no_installment"] +
        params["max_installment"] +
        params["currency"] +
        params["test_mode"] +
        PAYTR_MERCHANT_SALT
    )
    token = hmac.new(
        PAYTR_MERCHANT_KEY.encode("utf-8"),
        hash_str.encode("utf-8"),
        hashlib.sha256
    ).digest()
    params["paytr_token"] = base64.b64encode(token).decode()

    # PayTR'ye POST at
    try:
        post_data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(
            "https://www.paytr.com/odeme/api/get-token",
            data=post_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
    except Exception as e:
        app.logger.exception("PayTR token hatası")
        return _cors(jsonify({"error": str(e)})), 500

    if result.get("status") == "success":
        app.logger.info("PayTR token alındı | oid=%s | paket=%s", merchant_oid, package)
        return _cors(jsonify({"token": result["token"], "merchant_oid": merchant_oid}))
    else:
        app.logger.error("PayTR hata: %s", result)
        return _cors(jsonify({"error": result.get("reason", "PayTR hatası")})), 500


@app.route("/api/paytr-callback", methods=["POST", "GET"])
def paytr_callback():
    """
    PayTR ödeme sonucu bildirimi (server-to-server).
    PayTR bu endpoint'i hem başarı hem başarısızlıkta çağırır.
    """
    # PayTR test modunda ok/fail URL'e GET redirect yapabilir — sadece 200 dön
    if request.method == "GET":
        return "OK", 200

    data = request.form

    merchant_oid   = data.get("merchant_oid", "")
    status         = data.get("status", "")
    total_amount   = data.get("total_amount", "")
    hash_received  = data.get("hash", "")

    # Hash doğrula
    hash_str = merchant_oid + PAYTR_MERCHANT_SALT + status + total_amount
    expected = base64.b64encode(
        hmac.new(
            PAYTR_MERCHANT_KEY.encode("utf-8"),
            hash_str.encode("utf-8"),
            hashlib.sha256
        ).digest()
    ).decode()

    if hash_received != expected:
        app.logger.warning("PayTR callback hash uyuşmadı | oid=%s", merchant_oid)
        return "PAYTR_INVALID_HASH", 400

    if status == "success":
        app.logger.info("✅ Ödeme başarılı | oid=%s | tutar=%s", merchant_oid, total_amount)
        # Tutar kuruştan TL'ye çevir
        try:
            amount_tl = int(total_amount) / 100
            amount_str = f"{amount_tl:,.0f} TL".replace(",", ".")
        except Exception:
            amount_str = total_amount + " kuruş"
        try:
            send_payment_email({
                "merchant_oid": merchant_oid,
                "amount_str":   amount_str,
                "email":        data.get("email", "—"),
                "package":      data.get("user_basket", "—"),
            })
        except Exception:
            app.logger.exception("Ödeme maili gönderilemedi")
    else:
        app.logger.warning("❌ Ödeme başarısız | oid=%s", merchant_oid)

    # PayTR "OK" yanıtı bekliyor — aksi halde tekrar dener
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
