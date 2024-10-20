FROM python:3.11-slim

ARG APP_VERSION

WORKDIR /tmp

COPY dist /tmp/dist

RUN pip install uv

RUN uv pip install --system --upgrade pip && \
    uv pip install -system /tmp/dist/*.whl

COPY requirements.txt /tmp/requirements.txt

RUN uv pip install --system -r requirements.txt

WORKDIR /root

COPY tests /root/tests
COPY app /root/app
COPY version.txt /root/version.txt
RUN mkdir log

ENV APP_VERSION=$APP_VERSION

EXPOSE 8000