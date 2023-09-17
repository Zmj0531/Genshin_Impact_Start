import os
import time
import cv2
import subprocess
import numpy as np
import pyautogui
import win32com.client
import win32con
import win32gui
import pygame
from PIL import ImageGrab
from pydub import AudioSegment

def is_genshin_running():
    return os.system('tasklist /FI "image eq YuanShen.exe" 2>NUL | find /I /N "YuanShen.exe">NUL') == 0

def get_genshin_install_dir():
    path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\原神\原神.lnk'
    shell = win32com.client.Dispatch("WScript.Shell")
    path = shell.CreateShortCut(path)
    return os.path.dirname(path.TargetPath)

def segment_startup_music():
    script_dir = os.path.dirname(__file__)
    music_path = os.path.join(script_dir, 'resources', 'Shed A Light.mp3')
    # 截取音乐的第1分15秒到1分35秒部分
    audio = AudioSegment.from_mp3(music_path)
    audio = audio[75*1000:95*1000]  # 截取时间段
    output_path = os.path.join(script_dir, 'resources', '启动的小曲.mp3')
    audio.export(output_path, format="mp3")  # 导出截取后的音乐文件

def play_startup_music():
    script_dir = os.path.dirname(__file__)
    music_path = os.path.join(script_dir, 'resources', '启动的小曲.mp3')
    if not os.path.exists(music_path):  # 判断截取后的音乐文件是否存在
        segment_startup_music()
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # 等待音乐播放完毕结束程序
        pygame.time.Clock().tick(10)

def create_transition_window(screen_width, screen_height):
    white_image = np.full((screen_height, screen_width, 3), 255, dtype=np.uint8)
    cv2.namedWindow('Transition', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Transition', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Transition', white_image)
    hwnd = win32gui.FindWindow(None, "Transition")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, screen_width, screen_height, win32con.SWP_SHOWWINDOW)
    return hwnd, white_image  # 返回白色画面

def blend_transition(screen, white_image, alpha):
    return cv2.addWeighted(screen, 1 - alpha, white_image, alpha, 0)

def main():
    if is_genshin_running():
        print("原神已启动！")
        os.system('pause')
        return

    screen_width, screen_height = pyautogui.size()
    pyautogui.FAILSAFE = False

    while True:
        screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))), cv2.COLOR_BGR2RGB)
        white_pixels = np.count_nonzero(screenshot >= [250, 250, 250])
        total_pixels = screenshot.shape[0] * screenshot.shape[1]
        white_percentage = white_pixels / total_pixels * 100
        print(f"屏幕白色区域 {white_percentage}%")

        if white_percentage >= 90:  # 判断白色区域 >=90% 启动原神
            break

    install_dir = get_genshin_install_dir()
    game_exe = os.path.join(install_dir, 'Genshin Impact Game', 'YuanShen.exe')

    transition_window, white_image = create_transition_window(screen_width, screen_height)  # 获取白色画面

    subprocess.Popen(game_exe)

    transition_steps = 35
    for step in range(transition_steps):
        alpha = (step + 1) / transition_steps
        screenshot = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))), cv2.COLOR_BGR2RGB)
        blended_image = blend_transition(screenshot, white_image, alpha)
        cv2.imshow('Transition', blended_image)
        cv2.waitKey(10)

    while True:
        windows = pyautogui.getWindowsWithTitle("原神")
        if windows:
            time.sleep(5)
            window = windows[0]
            pyautogui.moveTo(window.left, window.top)  # 将原神窗口置顶
            print(f"原神 启动!")
            play_startup_music()  # 播放启动音乐
            break

    time.sleep(1)
    cv2.destroyWindow('Transition')  # 结束创建的白色画面

if __name__ == "__main__":
    main()