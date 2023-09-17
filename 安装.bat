pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
pip install opencv-python
pip install pyautogui
pip install numpy
pip install pillow
pip install pywin32
pip install pygame
pip install pydub

mkdir "C:\Program Files\FFmpeg"
xcopy ".\resources\ffmpeg-5.1.2-essentials_build" "C:\Program Files\FFmpeg" /e /i /h /y
setx /M PATH "C:\Program Files\ffmpeg\bin;%PATH%"