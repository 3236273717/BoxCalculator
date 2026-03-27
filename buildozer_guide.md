# Buildozer 构建 APK 指南

## 方法一：在 Linux 系统上安装 Buildozer

### 1. 安装依赖

在 Ubuntu/Debian 系统上：

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
sudo pip3 install --upgrade pip setuptools virtualenv
```

### 2. 安装 Buildozer

```bash
sudo pip3 install buildozer
```

### 3. 初始化项目

```bash
# 进入项目目录
cd /path/to/your/project

# 初始化 Buildozer 配置
buildozer init

# 修改 buildozer.spec 文件（如果需要）
# 主要修改应用标题、包名、依赖等
```

### 4. 构建 APK

```bash
# 构建调试版本
buildozer android debug

# 构建发布版本
buildozer android release
```

## 方法二：使用 WSL（Windows Subsystem for Linux）

### 1. 安装 WSL

在 Windows 10/11 上：

1. 打开 PowerShell 作为管理员
2. 运行以下命令：

```powershell
wsl --install
```

3. 重启电脑
4. 打开 Microsoft Store，搜索并安装 Ubuntu（推荐 20.04 LTS 或 22.04 LTS）

### 2. 配置 WSL

1. 启动 Ubuntu
2. 设置用户名和密码
3. 更新系统：

```bash
sudo apt update && sudo apt upgrade -y
```

### 3. 安装依赖

```bash
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
sudo pip3 install --upgrade pip setuptools virtualenv
```

### 4. 安装 Buildozer

```bash
sudo pip3 install buildozer
```

### 5. 复制项目到 WSL

在 PowerShell 中运行：

```powershell
# 复制项目到 WSL
cp -r "C:\Users\32362\Desktop\新建文件夹 (2)" "\\wsl$\Ubuntu\home\your-username\"
```

### 6. 构建 APK

在 WSL 中：

```bash
# 进入项目目录
cd /home/your-username/新建文件夹 (2)

# 构建 APK
buildozer android debug
```

## 方法三：使用虚拟机

### 1. 安装虚拟机软件

- VMware Workstation Player（免费）
- VirtualBox（免费）

### 2. 下载 Linux 镜像

推荐使用 Ubuntu 20.04 LTS 或 22.04 LTS。

### 3. 创建虚拟机

1. 打开虚拟机软件
2. 创建新虚拟机
3. 选择下载的 Linux 镜像
4. 配置虚拟机（至少 4GB RAM，20GB 硬盘空间）

### 4. 安装 Linux

按照安装向导完成 Linux 安装。

### 5. 安装依赖和 Buildozer

参考方法一中的步骤 1-2。

### 6. 复制项目到虚拟机

使用共享文件夹或 SSH 等方式将项目文件复制到虚拟机中。

### 7. 构建 APK

参考方法一中的步骤 4。

## 注意事项

1. 第一次构建可能需要较长时间，因为需要下载和编译依赖项
2. 确保网络连接稳定
3. 构建过程中可能会遇到各种错误，需要根据错误信息进行排查
4. 构建完成后，APK 文件会生成在 `bin` 目录中

## 常见问题

### 1. 内存不足

解决方法：增加虚拟机或 WSL 的内存分配。

### 2. 依赖项缺失

解决方法：根据错误信息安装缺失的依赖项。

### 3. 构建失败

解决方法：查看详细的错误日志，根据日志信息进行排查。

### 4. 签名错误

解决方法：在 `buildozer.spec` 文件中配置签名信息，或使用自动签名。

## 构建成功后的操作

1. 在 `bin` 目录中找到生成的 APK 文件
2. 将 APK 文件传输到 Android 设备
3. 在设备上安装并测试应用