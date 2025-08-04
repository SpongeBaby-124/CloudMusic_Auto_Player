# 项目结构说明

## 重构后的文件组织

本项目已重构为模块化架构，各功能分离到不同模块中，便于维护和扩展。

```
CloudMusic_Auto_Player/
├── src/
│   ├── config/
│   │   ├── hotkeys.json          # 快捷键配置文件
│   │   └── README.md             # 配置说明文档
│   ├── utils/
│   │   ├── config_manager.py     # 配置管理模块
│   │   └── music_search.py       # 音乐搜索模块
│   ├── controllers/
│   │   ├── netease_controller.py # 网易云音乐基础控制器
│   │   └── daily_controller.py   # 每日推荐控制器
│   ├── chromedriver/
│   │   └── win64/
│   │       └── chromedriver.exe  # ChromeDriver
│   └── server.py                 # MCP服务器主文件
├── config.json                   # 兼容性配置文件
├── netease_config.json          # 网易云音乐配置
├── playlists.json               # 歌单配置
├── requirements.txt             # 依赖列表
└── PROJECT_STRUCTURE.md         # 本文件
```

## 模块说明

### 1. 配置管理 (`src/utils/config_manager.py`)

负责处理所有配置文件的加载、保存和管理：

- **快捷键配置管理**：跨平台快捷键加载和保存
- **歌单配置管理**：系统预设和用户自定义歌单
- **网易云音乐配置**：每日推荐功能相关配置
- **平台检测**：自动识别Windows/Mac/Linux

**主要功能**：
- `load_hotkeys_config()` - 加载快捷键配置
- `load_custom_playlists()` - 加载歌单配置
- `load_netease_config()` - 加载网易云音乐配置
- `get_platform()` - 获取当前平台

### 2. 音乐搜索 (`src/utils/music_search.py`)

处理网易云音乐的搜索和URL生成：

- **歌曲搜索**：基于网易云音乐API搜索歌曲
- **歌单搜索**：搜索网易云音乐歌单
- **URL生成**：生成orpheus://播放链接

**主要功能**：
- `search_netease_music()` - 搜索歌曲
- `search_netease_playlist()` - 搜索歌单
- `generate_play_url()` - 生成播放URL
- `generate_playlist_play_url()` - 生成歌单播放URL

### 3. 基础控制器 (`src/controllers/netease_controller.py`)

网易云音乐的基本控制功能：

- **URL Scheme启动**：使用orpheus://启动应用
- **全局快捷键控制**：发送全局快捷键
- **窗口管理**：最小化窗口功能
- **跨平台支持**：Windows/Mac平台适配

**主要功能**：
- `launch_by_url_scheme()` - URL启动应用
- `send_global_hotkey()` - 发送快捷键
- `update_hotkeys()` - 更新快捷键配置

### 4. 每日推荐控制器 (`src/controllers/daily_controller.py`)

基于Selenium的高级功能：

- **每日推荐播放**：使用固定路径策略
- **私人漫游功能**：VIP漫游功能启动
- **进程管理**：网易云音乐进程控制
- **状态检测**：播放状态和音乐信息获取

**主要功能**：
- `connect_to_netease()` - 连接到网易云音乐
- `play_daily_recommend()` - 播放每日推荐
- `play_roaming()` - 启动私人漫游

### 5. MCP服务器 (`src/server.py`)

MCP工具定义和服务器启动：

- **工具定义**：所有MCP工具的实现
- **错误处理**：统一的错误处理和返回格式
- **平台信息**：包含平台信息的响应
- **服务器启动**：main函数和服务器配置

## 配置文件说明

### 1. 快捷键配置 (`src/config/hotkeys.json`)

支持Windows和Mac的快捷键自定义：

```json
{
  "hotkeys": {
    "windows": {
      "play_pause": "ctrl+alt+p",
      "previous": "ctrl+alt+left",
      "next": "ctrl+alt+right"
    },
    "mac": {
      "play_pause": "cmd+alt+p",
      "previous": "cmd+alt+left", 
      "next": "cmd+alt+right"
    }
  },
  "custom_hotkeys": {
    "play_pause": "ctrl+space"
  }
}
```

### 2. 网易云音乐配置 (`netease_config.json`)

每日推荐功能配置：

```json
{
  "netease_music_path": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
  "debug_port": 9222,
  "chromedriver_path": "src/chromedriver/win64/chromedriver.exe"
}
```

### 3. 歌单配置 (`playlists.json`)

系统预设和用户自定义歌单：

```json
{
  "systemPlaylists": {
    "飙升榜": {"id": "19723756", "name": "音乐飙升榜"},
    "新歌榜": {"id": "3779629", "name": "音乐新歌榜"}
  },
  "userPlaylists": {
    "我的歌单": {"id": "123456", "name": "用户自定义歌单"}
  }
}
```

## 重构优势

### 1. 模块化设计
- 功能分离，职责清晰
- 易于维护和扩展
- 代码复用性高

### 2. 跨平台支持
- 自动平台检测
- 平台特定配置
- 统一的API接口

### 3. 配置灵活性
- 独立的配置文件
- 用户自定义支持
- 热配置更新

### 4. 错误处理
- 统一的错误格式
- 详细的错误信息
- 故障排除建议

## 使用指南

### 1. 快捷键自定义

1. 编辑 `src/config/hotkeys.json`
2. 在 `custom_hotkeys` 中添加配置
3. 重启MCP服务器

### 2. 每日推荐功能设置

1. 设置网易云音乐路径（二选一）：
   - 方式一：设置环境变量 `NETEASE_MUSIC_PATH`
   - 方式二：在 `netease_config.json` 中配置 `netease_music_path`
2. 确保ChromeDriver可用
3. 使用 `play_daily_recommend()` 播放

#### 环境变量设置方法

**Windows:**
```cmd
# 设置网易云音乐路径
set NETEASE_MUSIC_PATH=C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe

# 设置ChromeDriver路径（可选，项目已包含Windows版本）
set CHROMEDRIVER_PATH=C:\path\to\chromedriver.exe

# 永久设置（系统环境变量）
setx NETEASE_MUSIC_PATH "C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe"
setx CHROMEDRIVER_PATH "C:\path\to\chromedriver.exe"
```

**macOS/Linux:**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export NETEASE_MUSIC_PATH="/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
export CHROMEDRIVER_PATH="/opt/homebrew/bin/chromedriver"  # macOS with Homebrew

# 然后重新加载配置
source ~/.bashrc  # 或 source ~/.zshrc
```

**ChromeDriver安装说明：**
- **Windows**: 项目已包含ChromeDriver，通常无需额外安装
- **macOS**: `brew install chromedriver`
- **Linux**: 下载对应Chrome版本的ChromeDriver并放置到系统PATH中

### 3. 歌单管理

1. 使用 `manage_custom_playlists()` 管理歌单
2. 直接编辑 `playlists.json` 文件
3. 使用 `search_and_play_playlist()` 播放

## 开发说明

### 添加新功能

1. 确定功能归属模块
2. 在对应模块中实现功能
3. 在 `server.py` 中添加MCP工具
4. 更新配置文件（如需要）

### 添加新平台支持

1. 在 `config_manager.py` 中添加平台检测
2. 在 `hotkeys.json` 中添加平台配置
3. 在控制器中实现平台特定逻辑

### 测试建议

1. 测试所有平台的快捷键功能
2. 验证配置文件的加载和保存
3. 测试每日推荐和搜索功能
4. 检查错误处理和日志输出 