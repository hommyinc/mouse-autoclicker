# code created with ChatGPT 4o
# https://chatgpt.com/

import pyautogui
from pynput import keyboard, mouse
import threading
import time

from config import NUM_CLICK, INTERVAL

class AutoClicker:
    reading = False
    mouse_position = (0, 0)
    patience = 5

    @classmethod
    def get_mouse_position(cls, verbose=False):
        while cls.reading:
            cls.mouse_position = pyautogui.position()
            if verbose: print(cls.mouse_position)
    
    @classmethod
    def stop_func(cls, *args):
        cls.reading = False
        raise EOFError

    @classmethod
    def on_press(cls, key, verbose=False):
        try:
            if key.char == 'y':
                for i in range(cls.patience):
                    print(f"마우스 위치를 {cls.patience-i}초 뒤 추적합니다.")
                    time.sleep(1)
                print("중단하려면 클릭하세요.")
                cls.reading = True
                try:
                    with mouse.Listener(on_click=cls.stop_func) as listener:
                        threading.Thread(target=cls.get_mouse_position).start()
                        listener.join()
                except EOFError:
                    pass
                print(f"마우스 위치 저장 완료. 현재 위치: {cls.mouse_position}")
            elif key.char == 'q':
                print("프로그램 중단.")
                return False
            else:
                for i in range(cls.patience):
                    print(f"저장된 마우스 위치에 {cls.patience-i}초 뒤 클릭을 시작합니다.")
                    time.sleep(1)
                print(f"{NUM_CLICK}회 클릭을 실행합니다. 중단하려면 아무 키나 누르세요.")
                cls.reading = True
                try:
                    with keyboard.Listener(on_press=cls.stop_func) as listener:
                        for i in range(NUM_CLICK):
                            pyautogui.click(cls.mouse_position)
                            if verbose: print(i+1)
                            time.sleep(INTERVAL)
                            if not cls.reading: break
                        listener.join()
                except EOFError:
                    pass
                print("클릭 완료.")
        except KeyboardInterrupt:
            return False

def main():
    a = AutoClicker()
    with keyboard.Listener(on_press=a.on_press) as listener:
        listener.join()

if __name__ == "__main__":
    print("프로그램 시작. 'y'를 입력하면 마우스 위치를 추적하고, 'q'를 입력하면 프로그램을 중단, 그 외의 키를 누르면 클릭합니다.")
    main()
