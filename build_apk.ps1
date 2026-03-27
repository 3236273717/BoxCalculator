# Kivy APK 构建脚本 (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Kivy APK 构建脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Docker 是否安装
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker 未安装"
    }
    Write-Host "Docker 版本: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：Docker 未安装或未在 PATH 中" -ForegroundColor Red
    Write-Host "请访问 https://www.docker.com/get-started 下载并安装 Docker Desktop" -ForegroundColor Yellow
    Read-Host "按 Enter 键退出"
    exit 1
}

# 检查 Docker 是否正在运行
try {
    $dockerInfo = docker info 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker 服务未运行"
    }
    Write-Host "Docker 服务正在运行" -ForegroundColor Green
} catch {
    Write-Host "错误：Docker 服务未运行" -ForegroundColor Red
    Write-Host "请启动 Docker Desktop 并等待服务就绪" -ForegroundColor Yellow
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""
Write-Host "Docker 检查通过，开始构建..." -ForegroundColor Green
Write-Host ""

# 创建 bin 目录（如果不存在）
if (-not (Test-Path "bin")) {
    New-Item -ItemType Directory -Name "bin" | Out-Null
    Write-Host "创建 bin 目录" -ForegroundColor Green
}

# 构建 Docker 镜像
Write-Host "步骤 1/3: 构建 Docker 镜像..." -ForegroundColor Cyan
try {
    docker build -t kivy-builder .
    if ($LASTEXITCODE -ne 0) {
        throw "Docker 镜像构建失败"
    }
    Write-Host "Docker 镜像构建成功！" -ForegroundColor Green
} catch {
    Write-Host "错误：Docker 镜像构建失败" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""

# 运行容器构建 APK
Write-Host "步骤 2/3: 构建 APK（这可能需要较长时间，请耐心等待）..." -ForegroundColor Cyan
try {
    docker run --rm -v "${PWD}/bin:/app/bin" kivy-builder
    if ($LASTEXITCODE -ne 0) {
        throw "APK 构建失败"
    }
    Write-Host "APK 构建成功！" -ForegroundColor Green
} catch {
    Write-Host "错误：APK 构建失败" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""

# 检查 APK 文件
Write-Host "步骤 3/3: 检查生成的 APK 文件..." -ForegroundColor Cyan
$apkFiles = Get-ChildItem "bin\*.apk" -ErrorAction SilentlyContinue

if ($apkFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "构建成功！" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "APK 文件已生成在 bin 目录中：" -ForegroundColor Green
    $apkFiles | ForEach-Object { Write-Host $_.Name -ForegroundColor Yellow }
    Write-Host ""
    Write-Host "您可以将 APK 文件传输到 Android 设备进行安装" -ForegroundColor Green
} else {
    Write-Host "警告：未找到生成的 APK 文件" -ForegroundColor Yellow
    Write-Host "请检查构建日志了解详细信息" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按 Enter 键退出"