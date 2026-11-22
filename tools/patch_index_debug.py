with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = '<script>'
replacement = '''<script>
      (function() {
        window.__errors = [];
        window.addEventListener('error', function(e) {
          console.error('[CAPTURE-ERROR]', e.message, e.filename, e.lineno, e.error);
          window.__errors.push({type: 'error', message: e.message, filename: e.filename, lineno: e.lineno, stack: e.error ? e.error.stack : null});
        });
        window.addEventListener('unhandledrejection', function(e) {
          console.error('[CAPTURE-REJECTION]', e.reason);
          window.__errors.push({type: 'rejection', reason: String(e.reason), stack: e.reason ? (e.reason.stack || e.reason.message) : null});
        });
        const origFetch = window.fetch;
        window.fetch = async function(...args) {
          const res = await origFetch.apply(this, args);
          const origJson = res.json.bind(res);
          res.json = async function() {
            try {
              return await origJson();
            } catch (err) {
              console.error('[FETCH-JSON-FAIL]', args[0], err);
              window.__failedFetch = { url: args[0], status: res.status, err: err.message };
              throw err;
            }
          };
          return res;
        };
        const origParse = JSON.parse;
        JSON.parse = function(text, reviver) {
          try {
            return origParse.call(this, text, reviver);
          } catch (err) {
            console.error('[JSON-PARSE-FAIL]', text ? text.substring(0, 100) : text, err);
            window.__failedJsonParse = { text: text ? text.substring(0, 200) : text, err: err.message };
            throw err;
          }
        };
      })();
    </script>'''

idx = c.find(target)
if idx != -1:
    end_script = c.find('</script>', idx)
    c = c[:idx] + replacement + c[end_script+len('</script>'):]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Updated index.html with deep interceptor')
