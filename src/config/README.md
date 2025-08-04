# 配置说明文档

## 快捷键配置 (`hotkeys.json`)

此文件允许用户自定义网易云音乐MCP控制器的快捷键配置，支持Windows和Mac两个平台。

### 文件结构

```json
{
  "description": "网易云音乐MCP控制器快捷键配置",
  "platform_info": {
    "windows": {
      "modifier_keys": ["ctrl", "alt", "shift", "win"],
      "description": "Windows平台快捷键配置"
    },
    "mac": {
      "modifier_keys": ["cmd", "ctrl", "alt", "shift"],
      "description": "Mac平台快捷键配置"
    }
  },
  "hotkeys": {
    "windows": {
      "play_pause": "ctrl+alt+p",
      "previous": "ctrl+alt+left",
      "next": "ctrl+alt+right",
      "volume_up": "ctrl+alt+up",
      "volume_down": "ctrl+alt+down",
      "mini_mode": "ctrl+alt+m",
      "like_song": "ctrl+alt+l",
      "lyrics": "ctrl+alt+d"
    },
    "mac": {
      "play_pause": "command+option+p",
      "previous": "command+option+left",
      "next": "command+option+right",
      "volume_up": "command+option+up",
      "volume_down": "command+option+down",
      "mini_mode": "command+option+m",
      "like_song": "command+option+l",
      "lyrics": "command+option+d"
    }
  },
  "custom_hotkeys": {
    "description": "用户可以在这里定义自定义快捷键，将覆盖默认配置",
    "example": {
      "play_pause": "ctrl+space",
      "volume_up": "ctrl+shift+up"
    }
  }
}
```

### 如何自定义快捷键

1. **直接修改平台配置**：
   - 修改 `hotkeys.windows` 或 `hotkeys.mac` 中的快捷键
   - 这将为特定平台设置默认快捷键

2. **使用自定义快捷键**（推荐）：
   - 在 `custom_hotkeys` 部分添加你的快捷键配置
   - 这些配置会覆盖默认设置，且不会在更新时丢失

### 快捷键格式

快捷键使用 `+` 连接多个按键，支持的修饰键：

**Windows**:
- `ctrl` - Ctrl键
- `alt` - Alt键  
- `shift` - Shift键
- `win` - Windows键

**Mac**:
- `command` - Command键
- `ctrl` - Control键
- `option` - Option键
- `shift` - Shift键

**示例**:
```json
{
  "play_pause": "ctrl+space",
  "volume_up": "cmd+shift+up",
  "next": "ctrl+alt+right"
}
```

### 支持的动作

- `play_pause` - 播放/暂停
- `previous` - 上一首
- `next` - 下一首  
- `volume_up` - 音量增加
- `volume_down` - 音量减少
- `mini_mode` - 切换迷你模式
- `like_song` - 喜欢当前歌曲
- `lyrics` - 切换歌词显示

### 自定义配置示例

在 `custom_hotkeys` 中添加你的配置：

```json
{
  "custom_hotkeys": {
    "play_pause": "ctrl+space",
    "volume_up": "ctrl+shift+up",
    "volume_down": "ctrl+shift+down",
    "next": "ctrl+right",
    "previous": "ctrl+left"
  }
}
```

### 注意事项

1. 修改配置后需要重启MCP服务器才能生效
2. 确保快捷键不与其他应用程序冲突
3. 某些系统保留的快捷键可能无法使用
4. 建议在自定义前备份原配置文件

### 平台检测

系统会自动检测当前平台：
- Windows系统使用 `hotkeys.windows` 配置
- macOS系统使用 `hotkeys.mac` 配置  
- Linux系统默认使用Windows配置

### 故障排除

如果快捷键不工作：

1. 检查配置文件语法是否正确
2. 确认依赖库已安装：`pip install pyautogui`
3. 检查快捷键是否被其他程序占用
4. 重启MCP服务器
5. 查看控制台日志获取详细错误信息 