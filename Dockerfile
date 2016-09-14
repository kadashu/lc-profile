FROM registry.cn-hangzhou.aliyuncs.com/einplus/centos-base:20160730
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY . /app

RUN pip3.5 install -i https://pypi.mirrors.ustc.edu.cn/simple -r pip-reqs.txt \
    && npm config set registry https://registry.npm.taobao.org \
    && npm install --unsafe-perm

CMD ["python3.5", "-m", "lc_profile.main"]
