#!/usr/bin/env python3
"""
配置管理模块
负责处理所有配置文件的加载、保存和管理
"""

import os
import json
import platform
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_project_root() -> str:
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_platform() -> str:
    """获取当前平台"""
    system = platform.system().lower()
    if system == "darwin":
        return "mac"
    elif system == "windows":
        return "windows"
    else:
        return "linux"  # 默认使用windows配置

def load_hotkeys_config() -> Dict[str, Any]:
    """加载快捷键配置"""
    try:
        config_path = os.path.join(get_project_root(), "src", "config", "hotkeys.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            current_platform = get_platform()
            
            # 获取当前平台的快捷键配置
            platform_hotkeys = config.get("hotkeys", {}).get(current_platform, {})
            
            # 如果有自定义快捷键，合并配置
            custom_hotkeys = config.get("custom_hotkeys", {})
            if isinstance(custom_hotkeys, dict) and "description" not in custom_hotkeys:
                # 自定义快捷键覆盖默认配置
                platform_hotkeys.update(custom_hotkeys)
            
            logger.info(f"✅ 已加载 {current_platform} 平台快捷键配置，共 {len(platform_hotkeys)} 个")
            return platform_hotkeys
        else:
            logger.warning(f"快捷键配置文件不存在: {config_path}")
            return get_default_hotkeys()
            
    except Exception as e:
        logger.error(f"加载快捷键配置失败: {e}")
        return get_default_hotkeys()

def get_default_hotkeys() -> Dict[str, str]:
    """获取默认快捷键配置（根据平台）"""
    current_platform = get_platform()
    
    if current_platform == "mac":
        return {
            "play_pause": "cmd+alt+p",
            "previous": "cmd+alt+left",
            "next": "cmd+alt+right",
            "volume_up": "cmd+alt+up",
            "volume_down": "cmd+alt+down",
            "mini_mode": "cmd+alt+m",
            "like_song": "cmd+alt+l",
            "lyrics": "cmd+alt+d"
        }
    else:  # Windows or Linux
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

def save_hotkeys_config(hotkeys: Dict[str, str]) -> bool:
    """保存快捷键配置到自定义部分"""
    try:
        config_path = os.path.join(get_project_root(), "src", "config", "hotkeys.json")
        
        # 加载现有配置
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        # 更新自定义快捷键部分
        config["custom_hotkeys"] = hotkeys
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ 已保存自定义快捷键配置，共 {len(hotkeys)} 个")
        return True
        
    except Exception as e:
        logger.error(f"保存快捷键配置失败: {e}")
        return False

def load_playlists_from_file() -> Dict[str, Any]:
    """从playlists.json文件加载歌单配置"""
    try:
        playlists_path = os.path.join(get_project_root(), "playlists.json")
        if os.path.exists(playlists_path):
            with open(playlists_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            # 如果文件不存在，创建默认配置
            default_data = {
                "systemPlaylists": {
                    "飙升榜": {"id": "19723756", "name": "音乐飙升榜", "description": "网易云音乐官方飙升榜"},
                    "新歌榜": {"id": "3779629", "name": "音乐新歌榜", "description": "网易云音乐官方新歌榜"},
                    "热歌榜": {"id": "3778678", "name": "音乐热歌榜", "description": "网易云音乐官方热歌榜"},
                    "排行榜": {"id": "2250011882", "name": "音乐排行榜", "description": "网易云音乐官方排行榜"},
                    "原创榜": {"id": "2884035", "name": "原创音乐榜", "description": "网易云音乐官方原创榜"},
                    "私人雷达": {"id": "3136952023", "name": "私人雷达", "description": "网易云音乐个性化推荐"}
                },
                "userPlaylists": {}
            }
            save_playlists_to_file(default_data)
            return default_data
    except Exception as e:
        logger.error(f"加载歌单配置文件失败: {e}")
        return {"systemPlaylists": {}, "userPlaylists": {}}

def save_playlists_to_file(data: Dict[str, Any]) -> bool:
    """保存歌单配置到playlists.json文件"""
    try:
        playlists_path = os.path.join(get_project_root(), "playlists.json")
        with open(playlists_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存歌单配置文件失败: {e}")
        return False

def load_netease_config() -> Dict[str, Any]:
    """加载网易云音乐配置
    
    优先级顺序：
    1. 环境变量 NETEASE_MUSIC_PATH
    2. netease_config.json 文件中的配置
    3. 默认配置
    """
    try:
        config_path = os.path.join(get_project_root(), "netease_config.json")
        config = {}
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # 创建默认配置
            config = {
                "netease_music_path": "",
                "debug_port": 9222,
                "chromedriver_path": "src/chromedriver/win64/chromedriver.exe",
                "description": "网易云音乐配置文件 - 用于每日推荐播放功能",
                "notes": {
                    "netease_music_path": "网易云音乐客户端exe文件的完整路径，例如: C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe。也可以通过环境变量 NETEASE_MUSIC_PATH 设置",
                    "debug_port": "调试端口号，默认9222",
                    "chromedriver_path": "ChromeDriver的相对路径"
                }
            }
            save_netease_config(config)
        
        # 优先使用环境变量中的网易云音乐路径
        env_netease_path = os.environ.get("NETEASE_MUSIC_PATH")
        if env_netease_path:
            config["netease_music_path"] = env_netease_path
            logger.info(f"✅ 使用环境变量中的网易云音乐路径: {env_netease_path}")
        elif config.get("netease_music_path"):
            logger.info(f"✅ 使用配置文件中的网易云音乐路径: {config['netease_music_path']}")
        else:
            logger.warning("⚠️  网易云音乐路径未配置，请设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置")
        
        # 优先使用环境变量中的ChromeDriver路径
        env_chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
        if env_chromedriver_path:
            config["chromedriver_path"] = env_chromedriver_path
            logger.info(f"✅ 使用环境变量中的ChromeDriver路径: {env_chromedriver_path}")
        elif config.get("chromedriver_path"):
            # 如果配置文件中是相对路径，转换为绝对路径
            chromedriver_path = config["chromedriver_path"]
            if not os.path.isabs(chromedriver_path):
                chromedriver_path = os.path.join(get_project_root(), chromedriver_path)
                config["chromedriver_path"] = chromedriver_path
            logger.info(f"✅ 使用配置文件中的ChromeDriver路径: {config['chromedriver_path']}")
        else:
            # 默认路径，转换为绝对路径
            default_chromedriver = os.path.join(get_project_root(), "src/chromedriver/win64/chromedriver.exe")
            config["chromedriver_path"] = default_chromedriver
            logger.warning(f"⚠️  ChromeDriver路径未配置，使用默认路径: {default_chromedriver}")
        
        return config
        
    except Exception as e:
        logger.error(f"加载网易云音乐配置失败: {e}")
        # 异常情况下也要处理环境变量和绝对路径
        default_chromedriver = os.environ.get("CHROMEDRIVER_PATH")
        if not default_chromedriver:
            default_chromedriver = os.path.join(get_project_root(), "src/chromedriver/win64/chromedriver.exe")
        
        return {
            "netease_music_path": os.environ.get("NETEASE_MUSIC_PATH", ""),
            "debug_port": 9222,
            "chromedriver_path": default_chromedriver
        }

def save_netease_config(config: Dict[str, Any]) -> bool:
    """保存网易云音乐配置"""
    try:
        config_path = os.path.join(get_project_root(), "netease_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"保存网易云音乐配置失败: {e}")
        return False

def load_custom_playlists() -> Dict[str, str]:
    """获取用户自定义歌单（优先使用客户端配置，然后是独立配置文件，最后回退到config.json）"""
    try:
        # 从独立的playlists.json文件加载
        playlists_data = load_playlists_from_file()
        user_playlists = {}
        
        # 合并系统预设歌单和用户自定义歌单
        for name, info in playlists_data.get("systemPlaylists", {}).items():
            user_playlists[name] = info["id"]
        
        for name, info in playlists_data.get("userPlaylists", {}).items():
            user_playlists[name] = info["id"]
        
        if user_playlists:
            logger.info(f"从playlists.json加载歌单，共 {len(user_playlists)} 个")
            return user_playlists
        
        # 最后回退到config.json（向后兼容）
        config_path = os.path.join(get_project_root(), "config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                local_playlists = config.get("customPlaylists", {})
                if local_playlists:
                    logger.info(f"使用config.json的自定义歌单，共 {len(local_playlists)} 个")
                return local_playlists
        
        logger.info("未找到任何歌单配置")
        return {}
    except Exception as e:
        logger.warning(f"加载自定义歌单失败: {e}")
        return {} 