# 🎵 网易云音乐 MCP 控制器

一个基于网易云音乐MCP智能控制器，提供全局快捷键、搜索单曲播放、搜索歌单播放、自定义歌单管理、每日推荐和私人漫游等丰富功能。

## ✨ 主要特性

### 🎮 基础控制功能
- **启动网易云音乐**：支持 URL scheme 快速启动，可选自动最小化窗口
- **播放控制**：播放/暂停、上一首/下一首、音量调节
- **界面控制**：切换迷你模式、显示/隐藏歌词
- **互动功能**：一键喜欢当前歌曲

### 🎼 音乐搜索与播放
- **歌曲搜索播放**：直接搜索歌曲名或"歌曲名+歌手"组合播放
- **歌单搜索播放**：搜索并播放指定歌单
- **系统预设歌单**：快速播放飙升榜、新歌榜、热歌榜等官方榜单
- **私人雷达播放**：播放个性化推荐歌单

### 📋 歌单管理
- **自定义歌单管理**：添加、删除、列出用户自定义歌单
- **歌单配置文件**：支持通过 JSON 文件批量管理歌单
- **系统歌单集成**：内置官方热门榜单快速访问

### 🌟 高级功能
- **每日推荐播放**：自动播放网易云音乐每日推荐歌单
- **私人漫游**：启动网易云音乐私人漫游功能
- **全局快捷键**：支持全局快捷键控制，无需切换到音乐应用，支持按键自定义

### ⌨️ 全局快捷键支持

#### Windows 默认快捷键
- `Ctrl+Alt+P`：播放/暂停
- `Ctrl+Alt+Left`：上一首
- `Ctrl+Alt+Right`：下一首  
- `Ctrl+Alt+Up/Down`：音量加/减
- `Ctrl+Alt+M`：切换迷你模式
- `Ctrl+Alt+L`：喜欢当前歌曲
- `Ctrl+Alt+D`：显示/隐藏歌词

#### macOS 默认快捷键
- `command+option+P`：播放/暂停
- `command+option+Left`：上一首
- `command+option+Right`：下一首  
- `command+option+Up/Down`：音量加/减
- `command+option+M`：切换迷你模式
- `command+option+L`：喜欢当前歌曲
- `command+option+D`：显示/隐藏歌词

> 💡 可以在 `src/config/hotkeys.json` 的 `custom_hotkeys` 部分自定义快捷键

## 🔧 环境要求

### 通用要求
- **Python**：3.10+
- **网易云音乐客户端**：需安装并可正常运行
- **uv**：现代 Python 包管理器 ([安装指南](https://docs.astral.sh/uv/getting-started/installation/))

### 平台要求
- **Windows 10/11**：完整功能支持 ✅
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ✅
  - 私人漫游功能 ✅
  - 内置 ChromeDriver (Windows x64)
- **macOS 10.15+**：基础功能支持 ⚠️
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ❌ (不支持)
  - 私人漫游功能 ❌ (不支持)

## 📦 安装指南

### 1. 安装 uv（如果尚未安装）
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 克隆项目并安装依赖
```bash
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player
uv sync
```

### 3. macOS 说明
macOS 版本仅支持基础功能（全局快捷键控制、音乐搜索播放），不支持每日推荐和私人漫游功能。

### 主要依赖
- `fastmcp>=2.0.0`：MCP 服务器框架
- `pyautogui>=0.9.54`：跨平台全局快捷键支持
- `pywin32>=306`：Windows 系统集成（仅 Windows）
- `psutil>=5.9.0`：进程管理
- `selenium>=4.0.0`：Web 自动化（每日推荐/漫游功能）
- `requests>=2.28.0`：HTTP 请求库

## ⚙️ 配置说明

### 1. MCP 客户端配置

在你的 MCP 客户端配置文件中添加以下配置：

#### 方式一：使用 uvx（推荐）

直接使用已发布的 PyPI 包，无需下载源码：

```json
{
  "mcpServers": {
    "cloudmusic-auto-player": {
      "command": "uvx",
      "args": ["cloudmusic-auto-player==1.0.2"],
      "env": {
        "NETEASE_MUSIC_PATH": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
        "CHROMEDRIVER_PATH": "C:\\path\\to\\chromedriver.exe"
      }
    }
  }
}
```

**平台特定配置示例：**

**Windows 配置：**
```json
{
  "mcpServers": {
    "cloudmusic-auto-player": {
      "command": "uvx",
      "args": ["cloudmusic-auto-player==1.0.2"],
      "env": {
        "NETEASE_MUSIC_PATH": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
        "CHROMEDRIVER_PATH": "C:\\path\\to\\chromedriver.exe"
      }
    }
  }
}
```

**macOS 配置：**
```json
{
  "mcpServers": {
    "cloudmusic-auto-player": {
      "command": "uvx",
      "args": ["cloudmusic-auto-player==1.0.2"],
      "env": {
        "NETEASE_MUSIC_PATH": "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
      }
    }
  }
}
```

> 📝 **注意**：macOS 不支持每日推荐和私人漫游功能，因此无需配置 `CHROMEDRIVER_PATH`

#### 方式二：本地项目运行

如果你需要修改源码或本地开发，可以下载项目后使用：

```json
{
  "mcpServers": {
    "auto-music-player": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/CloudMusic_Auto_Player",
        "src/server.py"
      ],
      "cwd": "/path/to/CloudMusic_Auto_Player",
      "env": {
        "NETEASE_MUSIC_PATH": "/path/to/netease/music/executable",
        "CHROMEDRIVER_PATH": "/path/to/chromedriver"
      }
    }
  }
}
```

**Windows 本地项目示例：**
```json
{
  "mcpServers": {
    "auto-music-player": {
      "command": "uv",
      "args": [
        "run",
        "--project", 
        "C:\\Users\\YourName\\CloudMusic_Auto_Player",
        "src/server.py"
      ],
      "cwd": "C:\\Users\\YourName\\CloudMusic_Auto_Player",
      "env": {
        "NETEASE_MUSIC_PATH": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
        "CHROMEDRIVER_PATH": "C:\\Users\\YourName\\CloudMusic_Auto_Player\\src\\chromedriver\\win64\\chromedriver.exe"
      }
    }
  }
}
```

**macOS 本地项目示例：**
```json
{
  "mcpServers": {
    "auto-music-player": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "/Users/YourName/CloudMusic_Auto_Player/src/server.py"
      ],
      "cwd": "/Users/YourName/CloudMusic_Auto_Player",
      "env": {
        "NETEASE_MUSIC_PATH": "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
      }
    }
  }
}
```

> ⚠️ **重要提示**：
> - 请将路径替换为你的实际路径
> - Windows 路径中的反斜杠需要转义为 `\\`
> - macOS 不支持每日推荐和私人漫游功能
> - 配置完成后，建议调用 `get_netease_config()` 工具验证环境变量配置是否正确


### 2. 自定义歌单配置

#### 上传自定义歌单
可调用mcp上传自定义歌单，只需要输入歌单名称和歌单id即可（如有对歌单描述可添加）（推荐）
编辑项目根目录下的 `playlists.json` 文件：

```json
{
  "systemPlaylists": {
    "飙升榜": {"id": "19723756", "name": "音乐飙升榜", "description": "网易云音乐官方飙升榜"},
    "新歌榜": {"id": "3779629", "name": "音乐新歌榜", "description": "网易云音乐官方新歌榜"},
    "热歌榜": {"id": "3778678", "name": "音乐热歌榜", "description": "网易云音乐官方热歌榜"}
  },
  "userPlaylists": {
    "我的收藏": {"id": "123456789", "name": "我的收藏歌单", "description": "个人收藏"},
    "工作音乐": {"id": "987654321", "name": "工作专用歌单", "description": "适合工作时听的音乐"}
  }
}
```

**获取歌单 ID 的方法：**
1. 在网易云音乐网页版或客户端中打开歌单
2. 从 URL 中获取歌单 ID（例如：`https://music.163.com/#/playlist?id=123456789` 中的 `123456789`）
3. 将歌单信息添加到 `userPlaylists` 部分

## 🚀 使用方法
"""以下方法均推荐使用自然语言从agent调用mcp工具实现"""

### 基础播放控制

```python
# 启动网易云音乐
launch_netease_music(minimize_window=True)

# 播放控制
control_playback(action="play_pause")  # 播放/暂停
control_playback(action="next")        # 下一首
control_playback(action="previous")    # 上一首

# 音量控制
control_volume(action="volume_up")     # 音量加
control_volume(action="volume_down")   # 音量减

# 界面控制
toggle_mini_mode()  # 切换迷你模式
toggle_lyrics()     # 切换歌词显示
like_current_song() # 喜欢当前歌曲
```

### 音乐搜索与播放

```python
# 搜索并播放歌曲
search_and_play(query="稻香 周杰伦", minimize_window=True)

# 播放预设歌单
search_and_play_playlist(playlist_name="飙升榜", minimize_window=True)

# 播放自定义歌单
search_and_play_playlist(playlist_name="我的收藏", minimize_window=True)
```

### 高级功能

```python
# 播放每日推荐（需要先配置网易云音乐路径）
play_daily_recommend()

# 启动私人漫游（需要先配置网易云音乐路径）
play_roaming()

# 获取控制器信息和功能列表
get_controller_info()

# 获取当前配置（验证环境变量配置）
get_netease_config()
```

### 🔍 配置验证

配置完成后，强烈建议使用以下工具验证配置是否正确：

```python
# 验证环境变量和路径配置
get_netease_config()
```

该工具会返回：
- 当前网易云音乐路径配置状态
- ChromeDriver路径配置状态  
- 各路径文件是否存在
- 是否满足每日推荐功能的运行条件

**示例输出：**
```json
{
  "success": true,
  "config": {
    "netease_music_path": "你配置的网易云音乐路径",
    "path_status": "✅ 有效",
    "chromedriver_path": "你配置的chromedriver路径",
    "chromedriver_status": "✅ 存在",
    "platform": "windows"
  },
  "ready_for_daily_recommend": true
}
```

### 歌单管理

```python
# 列出所有歌单
manage_custom_playlists(action="list")

# 添加新歌单
manage_custom_playlists(
    action="add", 
    playlist_name="新歌单", 
    playlist_id="123456789", 
    description="歌单描述"
)

# 删除歌单
manage_custom_playlists(action="remove", playlist_name="旧歌单")
```

## ⚠️ 注意事项

### 重要提醒
1. **平台功能差异**：macOS 仅支持基础功能，不支持每日推荐和私人漫游
2. **网易云音乐路径配置**：Windows 用户使用每日推荐和私人漫游功能前，需要配置网易云音乐客户端路径（通过环境变量 `NETEASE_MUSIC_PATH` 设置）
3. **ChromeDriver要求**：Windows 每日推荐和漫游功能需要 ChromeDriver，项目已包含 Windows 版本
4. **VIP功能限制**：私人漫游功能可能需要网易云音乐 VIP 会员
5. **网络连接**：搜索和播放功能需要稳定的网络连接
6. **配置验证**：配置完成后，建议调用 `get_netease_config()` 工具验证环境变量配置是否正确

### 故障排除
- **快捷键不响应**：确保已安装 `pyautogui` 且没有其他程序占用快捷键
- **网易云音乐启动失败**：检查 URL scheme 是否正确注册，尝试重新安装网易云音乐
- **每日推荐无法播放**：确认网易云音乐路径配置正确，检查是否已登录账户
- **搜索功能异常**：检查网络连接，确认网易云音乐 API 可正常访问

### 兼容性说明

#### 支持的操作系统
- **Windows 10/11**：完整功能支持 ✅
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ✅
  - 私人漫游功能 ✅
  - 内置 ChromeDriver ✅

- **macOS 10.15+**：基础功能支持 ⚠️
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ❌ (不支持)
  - 私人漫游功能 ❌ (不支持)

#### 客户端要求
- 需要网易云音乐桌面客户端（不支持 UWP 版本）
- 建议使用最新版本的网易云音乐客户端以获得最佳兼容性
- macOS 用户推荐从官方网站下载桌面版本

## 📁 项目结构

```
auto_music/
├── src/
│   ├── server.py              # MCP 服务器主程序
│   └── chromedriver/          # ChromeDriver 文件
│       └── win64/
├── config.json                # MCP 客户端配置示例
├── netease_config.json        # 网易云音乐配置文件
├── playlists.json             # 歌单配置文件
└── README.md                  # 项目文档
```

## 🤝 技术支持

- **项目仓库**：https://github.com/SpongeBaby-124/CloudMusic_Auto_Player
- **问题反馈**：请在 GitHub Issues 中提交
- **联系邮箱**：lxd4094@foxmail.com

## 📄 许可证

本项目采用 MIT 许可证开源。

## 🔄 更新日志

### v1.0.2
- ✅ 添加uvx配置方式

---

**享受音乐，让控制更简单！** 🎵
