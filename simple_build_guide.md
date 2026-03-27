# 简单的 Kivy 应用打包方法

## 使用 Docker 容器构建 APK

Docker 是一种容器化技术，可以在 Windows 上运行包含所有必要依赖的 Linux 环境，从而简化 Buildozer 的构建过程。

### 步骤 1：安装 Docker

1. 访问 [Docker 官网](https://www.docker.com/get-started) 下载并安装 Docker Desktop for Windows
2. 安装完成后，启动 Docker Desktop
3. 确保 Docker 服务正在运行（右下角任务栏有 Docker 图标）

### 步骤 2：创建 Dockerfile

在项目目录中创建一个名为 `Dockerfile` 的文件：

```dockerfile
FROM ubuntu:22.04

# 安装依赖
RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip
RUN pip3 install --upgrade pip setuptools virtualenv

# 安装 Buildozer
RUN pip3 install buildozer

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 构建 APK
CMD ["buildozer", "android", "debug"]
```

### 步骤 3：构建 Docker 镜像

在项目目录中运行以下命令：

```powershell
# 构建 Docker 镜像
docker build -t kivy-builder .
```

### 步骤 4：运行 Docker 容器构建 APK

```powershell
# 运行容器并构建 APK
docker run --rm -v "${PWD}/bin:/app/bin" kivy-builder
```

构建完成后，APK 文件会生成在项目目录的 `bin` 文件夹中。

## 使用 Kivy Launcher（无需打包）

如果您只是想在 Android 设备上运行应用，而不需要生成独立的 APK，可以使用 Kivy Launcher。

### 步骤 1：在 Android 设备上安装 Kivy Launcher

1. 打开 Google Play Store
2. 搜索并安装 "Kivy Launcher"

### 步骤 2：准备应用文件

1. 在 Android 设备上创建一个名为 `Kivy` 的文件夹
2. 在 `Kivy` 文件夹中创建一个子文件夹，例如 `BoxCalculator`
3. 将以下文件复制到 `BoxCalculator` 文件夹中：
   - `kivy_calculator.py`
   - `main.py`

### 步骤 3：运行应用

1. 打开 Kivy Launcher 应用
2. 点击 `BoxCalculator` 文件夹
3. 应用将自动启动

## 使用在线构建服务

### 1. Buildozer Online

有些在线服务提供 Buildozer 构建功能，您可以上传项目文件，在线构建 APK。

### 2. GitHub Actions

如果您将项目托管在 GitHub 上，可以使用 GitHub Actions 来自动构建 APK。

#### 步骤 1：创建 GitHub Actions 配置文件

在项目目录中创建 `.github/workflows/build.yml` 文件：

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
        pip install --upgrade pip setuptools virtualenv
        pip install buildozer
    - name: Build APK
      run: |
        buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: apk
        path: bin/*.apk
```

#### 步骤 2：推送代码到 GitHub

将项目文件推送到 GitHub 仓库，GitHub Actions 会自动开始构建。

#### 步骤 3：下载 APK

构建完成后，您可以在 GitHub Actions 页面下载生成的 APK 文件。

## 注意事项

1. **Docker 方法**：首次构建可能需要较长时间，因为需要下载和编译依赖项，但后续构建会更快。

2. **Kivy Launcher 方法**：适用于测试和开发，但不适合发布应用。

3. **在线构建服务**：需要将代码上传到第三方服务，注意保护代码隐私。

## 推荐方法

如果您只是想快速测试应用，推荐使用 **Kivy Launcher** 方法。

如果您需要生成独立的 APK 文件，推荐使用 **Docker** 方法，因为它不需要手动设置 Linux 环境，且构建过程相对简单。

如果您的项目已经托管在 GitHub 上，推荐使用 **GitHub Actions** 方法，可以实现自动构建。