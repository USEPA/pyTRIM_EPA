# references; used these as tutorial plus a starting point, then made my own changes...
# https://docs.docker.com/get-started/02_our_app/
# https://simonwillison.net/2018/Nov/19/smaller-python-docker-images/

# START June 2024 - tfeiler switched to a newer MacBook with
# an Apple M2 chip -- and then the Docker container when running
# on AWS started throwing errors about "exec format error" when
# launching python3. Googled around and found:
# https://stackoverflow.com/questions/73398714/docker-fails-when-building-on-m1-macs-exec-usr-local-bin-docker-entrypoint-sh
# https://stackoverflow.com/questions/65612411/forcing-docker-to-use-linux-amd64-platform-by-default-on-macos/69636473#69636473
# https://docs.docker.com/build/building/multi-platform/
#
# fix appears to be adding --platform=linux/amd64 to the FROM
# commands to ensure we use the right architecture.
#
# before figuring this out -- or if you want to build an image
# that can run locally at some point -- I also was running into
# this error during docker build:
# ../../meson.build:82:0: ERROR: Unknown compiler(s): [['gfortran'], ['flang'], ['nvfortran'], ['pgfortran'], ['ifort'], ['ifx'], ['g95']]
# and then a bunch more. Fix was to manually install more libs
# for compilation purposes; I did this right after installing gcc/python3-dev/etc:
# RUN apk add gfortran openblas openblas-dev linux-headers libffi-dev
# following the --platform realization, we no longer need
# gfortran/openblas/etc. so I commented that out. But keeping it
# in here commented out in case we ever need to revisit.
# END June 2024

ARG PYTRIM_BUILD_PLATFORM="linux/amd64"

# FROM python:3.11-alpine as builder
# FROM --platform=linux/amd64 python:3.11-alpine AS builder
# FROM --platform=${PYTRIM_BUILD_PLATFORM} python:3.11-alpine
FROM --platform=${PYTRIM_BUILD_PLATFORM} qgis/qgis

# Set environment variables for QGIS
ENV QGIS_PREFIX_PATH=/usr
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

WORKDIR /app

#
# install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /app/runmodel_venv

# get a working setuptools
RUN /app/runmodel_venv/bin/pip install --upgrade setuptools

# need git for flask-api
RUN apt-get update && apt-get install -y git

# install TRIM specific packages
RUN /app/runmodel_venv/bin/pip install -r /tmp/requirements.txt

# don't need this normally - but useful if we want to connect and mess around...
# RUN apt install -y vim

# copy Trim source code in
COPY temp/ /app/pytrim_runmodel_src/

WORKDIR /app/pytrim_runmodel_src

# START - AWS
# note this is only when debugging, blah blah, dont need just to run the model
# pip3 install awscli --break-system-packages
#
# if you want to run, go to blah blah
# export AWS_DEFAULT_REGION=us-east-1
# END - AWS


# A) run bash (no need to install) to let us peek around by attaching
# CMD ["bash"]

# B) or, run the actual PyTrim simulator code and quit when done
# uses the virtual environment
CMD ["/app/runmodel_venv/bin/python3", "docker_entrypoint.py"]
