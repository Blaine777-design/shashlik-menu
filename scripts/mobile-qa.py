"""Run real mobile viewport checks through Chrome DevTools on port 9222."""
import base64, json, time
from pathlib import Path
import requests, websocket

root = Path(__file__).resolve().parents[1]
out = root / "qa-mobile"
out.mkdir(exist_ok=True)
page = requests.get("http://127.0.0.1:9222/json", timeout=5).json()[0]
ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=15)
counter = 0
def call(method, params=None):
    global counter
    counter += 1
    ws.send(json.dumps({"id": counter, "method": method, "params": params or {}}))
    while True:
        message = json.loads(ws.recv())
        if message.get("id") == counter:
            return message.get("result", {})

checks = []
for width in (320, 360, 375, 390, 414, 430, 768):
    call("Emulation.setDeviceMetricsOverride", {"width": width, "height": 900, "deviceScaleFactor": 1, "mobile": True})
    call("Page.navigate", {"url": "http://127.0.0.1:4173"})
    time.sleep(2)
    call("Runtime.evaluate", {"expression": "document.querySelectorAll('img').forEach(i=>{i.loading='eager';i.src=i.src})"})
    time.sleep(2)
    expression = """(()=>{const html=document.documentElement,s=document.querySelector('#search');
      const initial=document.querySelectorAll('.dish').length;
      s.value='борщ';s.dispatchEvent(new Event('input',{bubbles:true}));
      const searchCount=document.querySelectorAll('.dish').length,searchName=document.querySelector('.dish strong')?.textContent;
      s.value='';s.dispatchEvent(new Event('input',{bubbles:true}));
      document.querySelector('.dish').click();const opened=document.querySelector('#dialog').classList.contains('open');
      document.querySelector('#close-dialog').click();const closed=!document.querySelector('#dialog').classList.contains('open');
      return {width:innerWidth,scrollWidth:html.scrollWidth,initial,searchCount,searchName,opened,closed,
        categories:document.querySelectorAll('.categories a').length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,
        sticky:getComputedStyle(document.querySelector('.menu-tools')).position};})()"""
    evaluated = call("Runtime.evaluate", {"expression": expression, "returnByValue": True})
    if "value" not in evaluated.get("result", {}):
        raise RuntimeError(evaluated)
    value = evaluated["result"]["value"]
    checks.append(value)
    shot = call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
    (out / f"menu-{width}.png").write_bytes(base64.b64decode(shot["data"]))
ws.close()
print(json.dumps(checks, ensure_ascii=False, indent=2))
