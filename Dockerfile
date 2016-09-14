FROM registry.cn-hangzhou.aliyuncs.com/einplus/centos-base:20160730
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY . /app
RUN pip3.5 install -i https://pypi.mirrors.ustc.edu.cn/simple -r pip-reqs.txt

CMD ["python3.5", "-m", "lc_profile.main"]
