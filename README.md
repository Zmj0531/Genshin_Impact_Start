# Genshin Impact Start
## 简介

这是一个整活向的程序（
创意来自于B站

**检测到屏幕白色占比超过90%将自动启动原神，并播放启动的小曲**

<br/>

## 技术实现

- 主程序基于Python语言实现
- 使用OpenCV库检测屏幕白色像素占比
- 使用pydub库中的AudioSegment，调用FFmpeg实现音频切片
- 使用pygame库播放启动的小曲
- 通过调用开始菜单原神快捷方式启动，并将窗口置顶

<br/>

## 使用说明

### 从源码使用:

使用管理员身份打开终端

```
git clone https://github.com/Zmj0531/Genshin_Impact_Start.git
cd Genshin_Impact_Start
start 安装.bat
start 原神 启动.bat
```

### 从Releases下载:

- 下载解压，安装后运行原神启动即可
