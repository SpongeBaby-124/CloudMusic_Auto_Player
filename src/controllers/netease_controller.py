#!/usr/bin/env python3
"""
网易云音乐控制器模块
负责网易云音乐的基本控制功能：启动、快捷键控制、窗口管理等
"""

import subprocess
import os
import sys
import time
import logging
import webbrowser
from typing import Dict, Optional

# 尝试导入全局快捷键库
try:
    import pyautogui
    HOTKEY_AVAILABLE = True
    # 禁用PyAutoGUI的fail-safe功能，支持全局快捷键
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.1
except ImportError as e:
    HOTKEY_AVAILABLE = False

# 尝试导入Windows窗口控制库
try:
    import win32gui
    import win32con
    WINDOW_CONTROL_AVAILABLE = True
except ImportError as e:
    WINDOW_CONTROL_AVAILABLE = False

logger = logging.getLogger(__name__)

class NeteaseMusicController:
    """网易云音乐控制器 - 简化版"""
    
    def __init__(self, hotkeys: Optional[Dict[str, str]] = None):
        """
        初始化控制器
        
        Args:
            hotkeys: 快捷键配置字典，如果为None则使用默认配置
        """
        # 设置快捷键配置
        self.hotkeys = hotkeys or self._get_default_hotkeys()
        
        # URL scheme 配置
        self.url_schemes = {
            "open": "orpheus://",
            "song": "orpheus://song/{song_id}",
            "playlist": "orpheus://playlist/{playlist_id}",
            "artist": "orpheus://artist/{artist_id}",
            "radio": "orpheus://radio",
            "recognize": "orpheuswidget://recognize",
            "downloads": "orpheuswidget://download"
        }
        
        logger.info(f"✅ 网易云音乐控制器初始化完成，快捷键数量: {len(self.hotkeys)}")
    
    def _get_default_hotkeys(self) -> Dict[str, str]:
        """获取默认快捷键配置"""
        return {
            "play_pause": "ctrl+alt+p",
            "previous": "ctrl+alt+left", 
            "next": "ctrl+alt+right",
            "volume_up": "ctrl+alt+up",
            "volume_down": "ctrl+alt+down",
            "mini_mode": "ctrl+alt+m",
            "like_song": "ctrl+alt+l",
            "lyrics": "ctrl+alt+d"
        }
    
    def update_hotkeys(self, new_hotkeys: Dict[str, str]) -> None:
        """更新快捷键配置"""
        self.hotkeys.update(new_hotkeys)
        logger.info(f"✅ 快捷键配置已更新，当前配置: {self.hotkeys}")
    
    def launch_by_url_scheme(self, scheme_url: str, minimize_window: bool = False) -> bool:
        """使用 URL scheme 启动网易云音乐"""
        try:
            logger.info(f"启动 URL scheme: {scheme_url}")
            
            # macOS 支持
            if sys.platform == 'darwin':
                try:
                    subprocess.run(["open", scheme_url], check=True)
                    logger.info("macOS open 命令启动成功")
                    # macOS 不支持简单的窗口最小化控制，这里略过
                    return True
                except Exception as e:
                    logger.warning(f"macOS open 命令失败: {e}")

            # 方法1: 使用 os.startfile (Windows 推荐)
            try:
                if hasattr(os, 'startfile'):
                    os.startfile(scheme_url)
                    logger.info("URL scheme 启动成功")
                    
                    # 如果需要最小化窗口
                    if minimize_window:
                        time.sleep(1.5)  # 等待窗口出现
                        self._minimize_netease_window()
                    
                    return True
            except Exception as e:
                logger.warning(f"os.startfile 失败: {e}")
            
            # 方法2: 使用 subprocess (Windows cmd)
            if sys.platform == 'win32':
                try:
                    subprocess.run(["cmd", "/c", "start", scheme_url], shell=True, check=True, timeout=5)
                    logger.info("subprocess 启动成功")
                    
                    if minimize_window:
                        time.sleep(1.5)
                        self._minimize_netease_window()
                    
                    return True
                except Exception as e:
                    logger.warning(f"subprocess 失败: {e}")
            
            # 方法3: 使用 webbrowser
            try:
                webbrowser.open(scheme_url)
                logger.info("webbrowser 启动成功")
                
                if minimize_window and sys.platform == 'win32':
                    time.sleep(1.5)
                    self._minimize_netease_window()
                
                return True
            except Exception as e:
                logger.warning(f"webbrowser 失败: {e}")
            
            return False
            
        except Exception as e:
            logger.error(f"URL scheme 启动失败: {e}")
            return False
    
    def _minimize_netease_window(self) -> bool:
        """查找并最小化网易云音乐窗口"""
        try:
            if not WINDOW_CONTROL_AVAILABLE:
                logger.warning("窗口控制功能不可用，无法最小化窗口")
                return False
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    
                    # 获取进程名称
                    try:
                        import win32process
                        import psutil
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        process = psutil.Process(pid)
                        process_name = process.name().lower()
                        
                        # 检查是否是网易云音乐进程
                        if process_name == "cloudmusic.exe" or "cloudmusic" in process_name:
                            windows.append((hwnd, window_title))
                    except:
                        # 如果无法获取进程信息，回退到窗口标题检查
                        app_keywords = ["网易云音乐", "NetEase", "CloudMusic", "NeteaseCloudMusic"]
                        if any(keyword in window_title for keyword in app_keywords):
                            windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            minimized_count = 0
            for hwnd, title in windows:
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    logger.info(f"已最小化窗口: {title}")
                    minimized_count += 1
                except Exception as e:
                    logger.warning(f"最小化窗口失败 {title}: {e}")
            
            if minimized_count > 0:
                return True
            else:
                logger.warning("未找到网易云音乐窗口")
                return False
            
        except Exception as e:
            logger.error(f"最小化窗口失败: {e}")
            return False
    
    def send_global_hotkey(self, action: str) -> bool:
        """发送全局快捷键"""
        try:
            if not HOTKEY_AVAILABLE:
                logger.error("快捷键功能不可用")
                return False
            
            if action not in self.hotkeys:
                logger.error(f"不支持的快捷键动作: {action}")
                return False
            
            hotkey = self.hotkeys[action]
            logger.info(f"发送全局快捷键: {hotkey} (动作: {action})")
            
            # 发送全局快捷键（无需窗口激活）
            pyautogui.hotkey(*hotkey.split('+'))
            time.sleep(0.1)
            
            return True
            
        except Exception as e:
            logger.error(f"发送快捷键失败: {e}")
            return False
    
    def get_supported_actions(self) -> list:
        """获取支持的动作列表"""
        return list(self.hotkeys.keys())
    
    def get_hotkey_for_action(self, action: str) -> Optional[str]:
        """获取指定动作的快捷键"""
        return self.hotkeys.get(action)
    
    def is_hotkey_available(self) -> bool:
        """检查快捷键功能是否可用"""
        return HOTKEY_AVAILABLE
    
    def is_window_control_available(self) -> bool:
        """检查窗口控制功能是否可用"""
        return WINDOW_CONTROL_AVAILABLE