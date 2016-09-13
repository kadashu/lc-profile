FROM python:3.5.1
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY . /app
RUN pip install -i https://pypi.mirrors.ustc.edu.cn/simple -r pip-reqs.txt

CMD ["python", "-m", "lc_profile.main"]
