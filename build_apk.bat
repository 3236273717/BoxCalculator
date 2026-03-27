@echo off
echo ==========================================
echo Kivy APK 构建脚本
echo ==========================================
echo.

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo 错误：Docker 未安装或未在 PATH 中
    echo 请访问 https://www.docker.com/get-started 下载并安装 Docker Desktop
    pause
    exit /b 1
)

REM 检查 Docker 是否正在运行
docker info >nul 2>&1
if errorlevel 1 (
    echo 错误：Docker 服务未运行
    echo 请启动 Docker Desktop 并等待服务就绪
    pause
    exit /b 1
)

echo Docker 检查通过，开始构建...
echo.

REM 创建 bin 目录（如果不存在）
if not exist bin mkdir bin

REM 构建 Docker 镜像
echo 步骤 1/3: 构建 Docker 镜像...
docker build -t kivy-builder .
if errorlevel 1 (
    echo 错误：Docker 镜像构建失败
    pause
    exit /b 1
)
echo Docker 镜像构建成功！
echo.

REM 运行容器构建 APK
echo 步骤 2/3: 构建 APK（这可能需要较长时间，请耐心等待）...
docker run --rm -v "%CD%\bin:/app/bin" kivy-builder
if errorlevel 1 (
    echo 错误：APK 构建失败
    pause
    exit /b 1
)
echo APK 构建成功！
echo.

REM 检查 APK 文件
echo 步骤 3/3: 检查生成的 APK 文件...
if exist bin\*.apk (
    echo.
    echo ==========================================
    echo 构建成功！
    echo ==========================================
    echo APK 文件已生成在 bin 目录中：
    dir bin\*.apk /b
    echo.
    echo 您可以将 APK 文件传输到 Android 设备进行安装
) else (
    echo 警告：未找到生成的 APK 文件
    echo 请检查构建日志了解详细信息
)

echo.
pause