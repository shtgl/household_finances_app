// Helper to set bullet ✔/✖
function setBullet(el, ok) {
  const bullet = el.querySelector('.rule-bullet');
  if (!bullet) return;
  bullet.textContent = ok ? '✔' : '✖';
  el.style.color = ok ? 'green' : '#333';
}

// Password rules
function attachPasswordHints(passwordEl, hintEl) {
  if (!passwordEl || !hintEl) return;
  const ruleList = hintEl.querySelectorAll('li');

  const checkRules = (value) => {
    const rules = {
      length: value.length >= 8,
      upper: /[A-Z]/.test(value),
      lower: /[a-z]/.test(value),
      digit: /[0-9]/.test(value),
      symbol: /[^A-Za-z0-9]/.test(value),
      norepeat: !/(.)\1{3,}/.test(value),
      noseq: !/(?:abc|bcd|cde|def|efg|fgh|123|234|345|456|567|678|789|890|098|876|765)/i.test(value)
    };
    ruleList.forEach(li => {
      const key = li.getAttribute('data-rule');
      setBullet(li, !!rules[key]);
    });
  };

  passwordEl.addEventListener('focus', () => hintEl.style.display = 'block');
  passwordEl.addEventListener('input', e => checkRules(e.target.value));
  passwordEl.addEventListener('blur', () => setTimeout(() => hintEl.style.display = 'none', 200));
}

// Name rules (first name / last name)
function attachNameHints(nameEl, hintEl, prefix) {
  if (!nameEl || !hintEl) return;

  const checkRules = () => {
    const val = nameEl.value || '';
    const rules = {
      notempty: val.trim().length > 0,
      capital: /^[A-Z]/.test(val),
      alpha: /^[A-Za-z]+$/.test(val)
    };
    hintEl.querySelectorAll('li').forEach(li => {
      const key = li.getAttribute(`data-${prefix}-rule`);
      setBullet(li, !!rules[key]);
    });
  };

  nameEl.addEventListener('focus', () => hintEl.style.display = 'block');
  nameEl.addEventListener('input', checkRules);
  nameEl.addEventListener('blur', () => setTimeout(() => hintEl.style.display = 'none', 200));
}

// Email rules
function attachEmailHints(emailEl, hintEl) {
  if (!emailEl || !hintEl) return;

  const checkRules = () => {
    const val = emailEl.value || '';
    const rules = {
      notempty: val.trim().length > 0,
      format: /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val),
      domain: /@.+\./.test(val)
    };
    hintEl.querySelectorAll('li').forEach(li => {
      const key = li.getAttribute('data-email-rule');
      setBullet(li, !!rules[key]);
    });
  };

  emailEl.addEventListener('focus', () => hintEl.style.display = 'block');
  emailEl.addEventListener('input', checkRules);
  emailEl.addEventListener('blur', () => setTimeout(() => hintEl.style.display = 'none', 200));
}

// Auto-init all hints on page
function initFormHints(config = {}) {
  const {passwords=[], names=[], emails=[]} = config;

  passwords.forEach(item => {
    if (item.confirm) {
      attachConfirmPasswordHints(item.el, item.hint, item.original);
    } else {
      attachPasswordHints(item.el, item.hint);
    }
  });
  names.forEach(item => attachNameHints(item.el, item.hint, item.prefix));
  emails.forEach(item => attachEmailHints(item.el, item.hint));
}

// Confirm password
function attachConfirmPasswordHints(confirmEl, hintEl, originalEl) {
  if (!confirmEl || !hintEl || !originalEl) return;
  const ruleList = hintEl.querySelectorAll('li');

  const checkMatch = () => {
    const match = confirmEl.value === originalEl.value && confirmEl.value.length > 0;
    ruleList.forEach(li => {
      const key = li.getAttribute('data-cpw-rule');
      if (key === 'match') setBullet(li, match);
    });
  };

  confirmEl.addEventListener('focus', () => hintEl.style.display = 'block');
  confirmEl.addEventListener('input', checkMatch);
  originalEl.addEventListener('input', checkMatch); // re-check if original password changes
  confirmEl.addEventListener('blur', () => setTimeout(() => hintEl.style.display = 'none', 200));
}