import random
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone

from app import base_logger
from .schema import User, db

from flask_login import (login_user, 
                         logout_user, 
                         login_required)
from flask import (Blueprint, 
                   render_template, 
                   redirect, 
                   url_for,
                   session, current_app, request)
from smtplib import SMTP, SMTP_SSL, SMTPException


bp = Blueprint("auth", __name__)


def _is_valid_name(name: str) -> tuple[bool, str]:
    """
    Validate a name: must start with a capital letter and contain only alphabets.
    """
    if not name:
        return False, 'Name is required.'
    
    if not name[0].isupper():
        return False, 'Name must start with a capital letter.'
    
    if not name.isalpha():
        return False, 'Name must contain only alphabetic characters (no spaces, hyphens, or apostrophes).'
    
    base_logger.info(f"{name} Validation: done")
    return True, ''


def _is_strong_password(pw: str) -> tuple[bool, str]:
    """Check password strength according to policy:
    - at least 8 characters
    - at least one lowercase, one uppercase, one digit, one symbol
    - no repeated characters (each character appears only once)
    - no sequences of 3 or more consecutive characters (ascending or descending)
    Returns (True, '') or (False, reason).
    """
    import string
    
    if not pw:
        return False, 'Password is required.'
        
    if len(pw) < 8:
        return False, 'Password must be at least 8 characters long.'
    
    has_lower = any(c.islower() for c in pw)
    has_upper = any(c.isupper() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_symbol = any(c in string.punctuation for c in pw)
   
    if not (has_lower and has_upper and has_digit and has_symbol):
        return False, 'Password must include uppercase, lowercase, digits and symbols.'
    
    if len(set(pw)) != len(pw):
        return False, 'Password must not contain repeated characters.'
    
    def _is_sequence(a, b, c):
        return (ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1) or (ord(b) == ord(a) - 1 and ord(c) == ord(b) - 1)

    for i in range(len(pw) - 2):
        if _is_sequence(pw[i], pw[i+1], pw[i+2]):
            return False, 'Password must not contain 3-character sequential runs (e.g. abc or 123).'

    base_logger.info(f"{pw} Validation: done")

    return True, ''


def _send_otp_via_email(to_addr: str, otp: str) -> bool:
    base_logger.info(f"Sending otp {otp} to address {to_addr}")
    """
    Send OTP to given address using current app mail config. Returns True on success.
    """
    cfg = current_app.config
    
    # Determine which SMTP settings to use
    domain = to_addr.split('@')[-1].lower()
    provider_cfg = domain
    
    # Use provider-specific settings, with a fallback to global config for each value
    mail_server = cfg.get('MAIL_SERVER')
    mail_port = int(cfg.get('MAIL_PORT', 587)) 
    mail_username = cfg.get('MAIL_USERNAME')
    mail_password = cfg.get('MAIL_PASSWORD')
    use_tls = cfg.get('MAIL_USE_TLS', True) 
    use_ssl = cfg.get('MAIL_USE_SSL', False) 
    

    html_content = render_template('emails/otp_email.html',
        app_name='Finance Management',
        greeting_message='Verify otp to Login',
        otp_digits=list(otp),
        otp_code=otp,
        tagline='Secure your finances',
        expiry_time=5,
        security_tips=[
            'Never share this code with anyone',
            'We will never ask for this code via phone or email',
            'If you didn\'t request this, please ignore this email'
        ],
        call_to_action='Enter this code in your Finance Management app to continue',
        team_name='Finance Management Team',
        footer_message='This is an automated message. Please do not reply to this email.'
    )
    
    # Plain text fallback
    plain_text = f"""
        Finance Management - Verification Required

        Your verification code is: {otp}

        This code will expire in 5 minutes.
        Keep this code confidential and do not share it with anyone.

        If you didn't request this code, please ignore this email.

        Best regards,
        Finance Management Team
    """

    msg = EmailMessage()
    msg['Subject'] = '🔐 Finance Management - Your Verification Code'
    msg['From'] = mail_username
    msg['To'] = to_addr
    
    # Set plain text content first
    msg.set_content(plain_text.strip())
    
    # Add HTML content as alternative
    msg.add_alternative(html_content.strip(), subtype='html')

    # Use different approaches based on SSL/TLS configuration
    if use_ssl:
        with SMTP_SSL(mail_server, mail_port, timeout=30) as smtp:
            smtp.ehlo()
            if mail_username and mail_password:
                smtp.login(mail_username, mail_password)
            smtp.send_message(msg)
    else:
        with SMTP(mail_server, mail_port, timeout=30) as smtp:
            smtp.ehlo()
            if use_tls:
                smtp.starttls()
                smtp.ehlo()  # Call ehlo() again after starttls()
            
            if mail_username and mail_password:
                smtp.login(mail_username, mail_password)
            smtp.send_message(msg)

    return True

def _get_user_from_session_otp():
    """Retrieves the user associated with the OTP verification session."""
    base_logger.info(f"Getting otp from user")
    user_id = session.get('otp_user_id')
    return User.query.get(int(user_id)) if user_id else None

# --- OTP-based password reset helpers & routes ---
def _start_reset_otp_for_user(user, minutes_valid=10):
    """Start a reset OTP flow for given user: stores otp and expiry in session and sends email."""
    otp = str(random.randint(100000, 999999)).zfill(6)
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=minutes_valid)).isoformat()
    session['reset_otp'] = otp
    session['reset_otp_expires_at'] = expires_at
    session['reset_otp_user_id'] = user.user_id
    session['reset_otp_attempts'] = 0
    base_logger.info(f"Started password reset OTP for user {user.email}; expires at {expires_at}")
    try:
        _send_otp_via_email(user.email, otp)
    except Exception:
        base_logger.exception("Failed to send password reset OTP email")
        # still keep session so user can retry; return False if you need special handling
    return True

def _get_user_from_session_reset_otp():
    user_id = session.get('reset_otp_user_id')
    return User.query.get(int(user_id)) if user_id else None

def _clear_reset_session():
    for k in ('reset_otp', 'reset_otp_expires_at', 'reset_otp_user_id', 'reset_otp_attempts', 'reset_verified'):
        session.pop(k, None)

@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Allows registered users to reset their forgotten password
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("forgot_password.html", info="If this email is registered, an OTP has been sent.")

        otp = str(random.randint(100000, 999999)).zfill(6)
        expires_at = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()

        session["reset_otp"] = otp
        session["reset_otp_expires"] = expires_at
        session["reset_user_id"] = user.user_id

        _send_otp_via_email(user.email, otp)

        return redirect(url_for("auth.verify_reset_otp"))

    return render_template("forgot_password.html")

@bp.route("/verify-reset-otp", methods=["GET", "POST"])
def verify_reset_otp():
    """
    Verifying the email-id makes sure, registered users only
    get the access of their accounts
    """
    if request.method == "POST":
        action = request.form.get("action")

        if action == "resend":
            user_id = session.get("reset_user_id")
            if not user_id:
                return redirect(url_for("auth.forgot_password"))

            user = User.query.get(user_id)
            otp = str(random.randint(100000, 999999)).zfill(6)
            session["reset_otp"] = otp
            session["reset_otp_expires"] = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
            _send_otp_via_email(user.email, otp)

            return render_template("verify_reset_otp.html", info="A new OTP has been sent to your email.")

        submitted = request.form.get("otp", "").strip()
        stored = session.get("reset_otp")
        expires_str = session.get("reset_otp_expires")
        user_id = session.get("reset_user_id")

        if not all([submitted, stored, expires_str, user_id]):
            return redirect(url_for("auth.forgot_password"))

        try:
            expires_dt = datetime.fromisoformat(expires_str)
        except (ValueError, TypeError):
            expires_dt = datetime.now(timezone.utc) - timedelta(seconds=1)

        if datetime.now(timezone.utc) > expires_dt:
            session.pop("reset_otp", None)
            session.pop("reset_otp_expires", None)
            session.pop("reset_user_id", None)
            return render_template("verify_reset_otp.html", error="OTP expired. Please try again.")

        if submitted == stored:
            return redirect(url_for("auth.reset_password"))
        else:
            return render_template("verify_reset_otp.html", error="Invalid OTP. Please try again.")

    return render_template("verify_reset_otp.html")


@bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """
    Provide new password, and confirm it to make sure
    the password is not forgotten again by us
    """
    user_id = session.get("reset_user_id")
    if not user_id:
        return redirect(url_for("auth.forgot_password"))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("reset_password.html", error="Passwords do not match.")

        ok, reason = _is_strong_password(password)
        if not ok:
            return render_template("reset_password.html", error=reason)

        user.set_password(password)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return render_template("reset_password.html", error="Something went wrong. Please try again.")

        # Clear reset session keys
        session.pop("reset_otp", None)
        session.pop("reset_otp_expires", None)
        session.pop("reset_user_id", None)

        return redirect(url_for("auth.login"))

    return render_template("reset_password.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Registers user on PostgreSQL database
    """
    if request.method == "POST":
        base_logger.info(f"Starting registration phase")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            return redirect(url_for("auth.register"))

        ok, reason = _is_valid_name(first_name)
        if not ok:
            return render_template('register.html')
        ok, reason = _is_valid_name(last_name)
        if not ok:
            return render_template('register.html')

        ok, reason = _is_strong_password(password)
        if not ok:
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            return render_template('register.html')

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Redirects to dashboard, after successful login
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        base_logger.info(f"Starting login phase")

        # validate credentials first
        if user and user.check_password(password):
            otp = str(random.randint(100000, 999999)).zfill(6)
            expires_at = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
            session['otp'] = otp
            session['otp_expires_at'] = expires_at
            session['otp_user_id'] = user.user_id
            session['next'] = request.args.get('next')

            sent = _send_otp_via_email(user.email, otp)
            if not sent:
                return redirect(url_for('auth.login'))

            return redirect(url_for('auth.verify'))

    return render_template("login.html")


@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """Verify OTP sent to user's email. 
    On success, log the user in and redirect to next/dashboard.
    """
    if request.method == 'POST':
        base_logger.info(f"Starting otp validation phase")
        action = request.form.get('action')

        if action == 'resend':
            user = _get_user_from_session_otp()
            if not user:
                return redirect(url_for('auth.login'))

            otp = str(random.randint(100000, 999999)).zfill(6)
            session['otp'] = otp
            session['otp_expires_at'] = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
            sent = _send_otp_via_email(user.email, otp)
            return redirect(url_for('auth.verify'))


        submitted = request.form.get('otp', '').strip()
        stored = session.get('otp')
        expires_str = session.get('otp_expires_at')
        user = _get_user_from_session_otp()

        if not all([submitted, stored, expires_str, user]):
            return redirect(url_for('auth.login'))

        try:
            expires_dt = datetime.fromisoformat(expires_str)
        except (ValueError, TypeError):
            expires_dt = datetime.now(timezone.utc) - timedelta(seconds=1) # Expired

        # clear session OTP info
        if datetime.now(timezone.utc) > expires_dt:
            session.pop('otp', None)
            session.pop('otp_expires_at', None)
            session.pop('otp_user_id', None)
            return redirect(url_for('auth.login'))

        if submitted == stored:
            # success - log user in
            # mark user verified and persist; always log the user in afterwards
            user.is_verified = True
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
            login_user(user)
            # clear OTP session keys
            session.pop('otp', None)
            session.pop('otp_expires_at', None)
            session.pop('otp_user_id', None)
            next_page = session.pop('next', None)
            return redirect(next_page or url_for('dashboard.dashboard'))
        else:
            return redirect(url_for('auth.verify'))

    # GET
    return render_template('verify.html')

@bp.route("/logout")
@login_required
def logout():
    """
    Allows user to log out or lock their account after visiting the page
    """
    logout_user()
    base_logger.info("Logged out successfully")
    return redirect(url_for("auth.login"))