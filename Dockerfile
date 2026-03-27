FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
ENV ANDROID_SDK_ROOT=/root/.buildozer/android/platform/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# 使用国内镜像源加速下载
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

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
    liblzma-dev \
    sqlite3 \
    libsqlite3-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libpng-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 升级 pip 并使用国内镜像
RUN pip3 install --upgrade pip setuptools virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 Buildozer
RUN pip3 install buildozer -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 构建 APK
CMD ["buildozer", "android", "debug"]
