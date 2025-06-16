import machine
import client
from lib.types import *
import time

CMD_SET_COLOR = 1
CMD_TOGGLE_ON_OFF = 2
CMD_SET_HOLIDAY = 3

def load_led_name():
    try:
        with open("name.txt", "r") as f:
            name = f.readline().strip()
            return name
    except:
        return "led1234"

class LedESP:
    def __init__(self, r_pin=2, g_pin=19, b_pin=21):
        self.pin_r = machine.Pin(r_pin, machine.Pin.OUT)
        self.pin_g = machine.Pin(g_pin, machine.Pin.OUT)
        self.pin_b = machine.Pin(b_pin, machine.Pin.OUT)

        self.pwm_r = machine.PWM(self.pin_r, freq=1000)
        self.pwm_g = machine.PWM(self.pin_g, freq=1000)
        self.pwm_b = machine.PWM(self.pin_b, freq=1000)

        self.rgb = (255, 255, 255)
        self.led_on = False
        self.holiday_mode = False

        self.recv_buffer = bytearray()
    
    def change_color(self, r, g, b):
        # Zakładam, że PWM 10-bit (0-1023), jasność skaluje odwrotnie (zależne od LED - jeśli odwrócone, zmień)
        self.pwm_r.duty(int((r / 255) * 1023))
        self.pwm_g.duty(int((g / 255) * 1023))
        self.pwm_b.duty(int((b / 255) * 1023))
        self.rgb = (r, g, b)
    
    def toggle_led(self):
        self.led_on = not self.led_on
        if self.led_on:
            self.change_color(*self.rgb)
        else:
            self.change_color(0, 0, 0)
    
    def set_holiday_mode(self, enable):
        self.holiday_mode = bool(enable)
    
    def handle_command(self ,msg):
        if not msg:
            return

        cmd = msg[0]

        if cmd == CMD_SET_COLOR:
            # oczekujemy 4 bajtów: [cmd, R, G, B]
            if len(msg) < 4:
                print("Błąd: za krótki pakiet dla SET_COLOR")
                return
            r, g, b = msg[1], msg[2], msg[3]
            print(f"Komenda SET_COLOR: R={r}, G={g}, B={b}")
            self.change_color(r, g, b)
        
        elif cmd == CMD_TOGGLE_ON_OFF:
            print("Komenda TOGGLE_ON_OFF")
            self.toggle_led()
        
        elif cmd == CMD_SET_HOLIDAY:
            # oczekujemy 2 bajty: [cmd, 0 lub 1]
            if len(msg) < 2:
                print("Błąd: za krótki pakiet dla SET_HOLIDAY")
                return
            enable = msg[1]
            print(f"Komenda SET_HOLIDAY: {enable}")
            self.set_holiday_mode(enable)
        
        else:
            print("Nieznana komenda:", cmd)
    
    def handle_data(self, data):
        self.recv_buffer.extend(data)

        while True:
            if len(self.recv_buffer) < 1:
                return

            cmd = self.recv_buffer[0]

            if cmd == CMD_SET_COLOR:
                needed_len = 4
            elif cmd == CMD_TOGGLE_ON_OFF:
                needed_len = 1
            elif cmd == CMD_SET_HOLIDAY:
                needed_len = 2
            else:
                print("Nieznana komenda, usuwam 1 bajt")
                del self.recv_buffer[0]
                continue

            if len(self.recv_buffer) < needed_len:
                return

            full_cmd = self.recv_buffer[:needed_len]
            del self.recv_buffer[:needed_len]

            self.handle_command(full_cmd)

    def handle_events(self):
        return

if __name__ == '__main__':
    led_esp = LedESP()
    cl = client.Client(tp=TYPE_LED, identity=load_led_name(), input_handler=led_esp)
    cl.prepare()

    try:
        while True:

            led_esp.handle_events()
            cl.pollEvents(timeout=0)
            time.sleep(0.05)
    except KeyboardInterrupt:
        cl.cleanup()
