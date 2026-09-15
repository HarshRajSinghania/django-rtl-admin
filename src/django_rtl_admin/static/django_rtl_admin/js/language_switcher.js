/*
 * Progressive enhancement for the admin language switcher.
 *
 * Without JavaScript the switcher is a plain <select> plus a submit button,
 * which works fine.  With JavaScript the button is redundant, so hide it and
 * submit on change instead.
 */
(function () {
  'use strict';

  function enhance(form) {
    var select = form.querySelector('.rtl-admin-language-switcher__select');
    var submit = form.querySelector('.rtl-admin-language-switcher__submit');
    if (!select || !submit) {
      return;
    }
    submit.hidden = true;
    select.addEventListener('change', function () {
      form.submit();
    });
  }

  function init() {
    var forms = document.querySelectorAll('.rtl-admin-language-switcher');
    for (var i = 0; i < forms.length; i++) {
      enhance(forms[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
