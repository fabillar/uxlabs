p='index.html'; s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:80],s.count(a)); s=s.replace(a,b)
rep('''      <button type="submit" class="btn btn-primary">Send message <svg class="ic"><use href="#i-arrow"/></svg></button>''',
'''      <div class="m-trap" aria-hidden="true"><label for="q-company">Company</label><input id="q-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
      <p class="m-error" id="quoteError" role="alert" hidden></p>
      <button type="submit" class="btn btn-primary" id="quoteSend"><span class="lbl">Send message</span> <svg class="ic"><use href="#i-arrow"/></svg></button>''')
rep('''<p>Your email app should be opening with your message ready to send. If nothing opens, just email us at <a href="mailto:hello@uxlabs.pro" data-direct>hello@uxlabs.pro</a> and we&rsquo;ll take it from there.</p>''',
'''<p>Your message is on its way. We&rsquo;ll get back to you within 1&ndash;2 business days. Need us sooner? Email <a href="mailto:hello@uxlabs.pro" data-direct>hello@uxlabs.pro</a>.</p>''')
rep('''  /* To receive submissions without an email app, paste a form-service URL here (e.g. Formspree or Web3Forms).
     While empty, sending composes an email to hello@uxlabs.pro. */
  var FORM_ENDPOINT = '';''','''  /* Submissions go to the Vercel function in /api/contact.js, which emails them through Resend. */
  var FORM_ENDPOINT = '/api/contact';''')
old_start=s.index("  qForm.addEventListener('submit', function(e){")
old_end=s.index("  /* Floating scroll-to-top button */")
s=s[:old_start]+r'''  var qErr = document.getElementById('quoteError'), qSend = document.getElementById('quoteSend');
  function showErr(msg){ qErr.innerHTML = msg; qErr.hidden = false; }
  qForm.addEventListener('submit', function(e){
    e.preventDefault();
    if(qSend.disabled) return;
    if(!qForm.checkValidity()){ qForm.reportValidity(); return; }
    qErr.hidden = true;
    var d = { name:qForm.name.value.trim(), email:qForm.email.value.trim(), phone:qForm.phone.value.trim(), service:qForm.service.value, message:qForm.message.value.trim(), company:qForm.company.value };
    var lbl = qSend.querySelector('.lbl'), was = lbl.textContent;
    qSend.disabled = true; qSend.classList.add('sending'); lbl.textContent = 'Sending…';
    fetch(FORM_ENDPOINT, { method:'POST', headers:{ 'Accept':'application/json', 'Content-Type':'application/json' }, body:JSON.stringify(d) })
      .then(function(r){ return r.json().catch(function(){ return {}; }).then(function(j){ if(!r.ok || !j.ok){ throw new Error(j.error || 'failed'); } }); })
      .then(function(){ modalEl.classList.add('sent'); qForm.reset(); })
      .catch(function(err){
        var m = err && err.message && err.message !== 'failed' && err.message.indexOf('fetch') === -1 ? err.message + ' ' : 'Sorry, your message couldn&rsquo;t be sent. ';
        showErr(m.replace(/</g,'&lt;').replace(/&lt;/g,'<').replace(/<(?!\/?(a|br)\b)/g,'&lt;') + 'You can also email us at <a href="mailto:hello@uxlabs.pro" data-direct>hello@uxlabs.pro</a>.');
      })
      .then(function(){ qSend.disabled = false; qSend.classList.remove('sending'); lbl.textContent = was; });
  });

'''+s[old_end:]
# styles
rep('.m-form .btn-primary{ width:100%; margin-top:2px; }',
'''.m-form .btn-primary{ width:100%; margin-top:2px; }
.m-form .btn-primary:disabled{ opacity:.75; cursor:progress; transform:none; }
.m-form .btn-primary.sending .ic{ animation:pfv-spin 1s linear infinite; }
.m-trap{ position:absolute; left:-9999px; width:1px; height:1px; overflow:hidden; }
.m-error{ margin:0; padding:10px 14px; border-radius:12px; font-size:13.5px; line-height:1.5; color:#b4235f; background:color-mix(in srgb, var(--magenta) 10%, var(--card)); border:1px solid color-mix(in srgb, var(--magenta) 30%, transparent); }
.m-error a{ color:inherit; font-weight:600; text-decoration:underline; }''')
open(p,'w',encoding='utf-8',newline='').write(s); print('ok')
