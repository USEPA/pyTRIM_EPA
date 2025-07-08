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
FROM --platform=${PYTRIM_BUILD_PLATFORM} python:3.11-alpine

# Install all the python libraries we need to run...Alpine lacks a compiler toolchain for building some things we need, like pandas.
RUN apk add --no-cache gcc python3-dev musl-dev alpine-sdk

# DON'T NEED THIS -- see above "June 2024" comment...
# RUN apk add gfortran openblas openblas-dev linux-headers libffi-dev

# START - some Python packages can't install/build via pip without some extra work.
# (pyproj)
RUN apk add --no-cache \
    proj \
    proj-data \
    proj-util \
    geos \
    geos-dev \
    g++ \
    libgcc \
    libstdc++ \
    libffi-dev \
    py3-pip

# END - some Python packages..

# Set env vars for pyproj in final image
ENV PROJ_LIB=/usr/share/proj

# OPTION 1 - Now build a fresh container, copying across the compiled pieces
# install Python packages
# COPY requirements.txt /tmp/requirements.txt
# RUN python3 -m pip install --upgrade pip
# RUN python3 -m pip install cython
# RUN python3 -m pip install -r /tmp/requirements.txt

# FROM python:3.11-alpine
# COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# OPTION 2 - if you want to log in and troubleshoot things, install and run bash instead of default...
# RUN apk add --no-cache bash
# CMD ["bash"]

# OPTION 3 - poc python script
# RUN python3 -m pip install boto3
# COPY pocpy/dummy.py /tmp/dummy.py
# CMD ["python3", "/tmp/dummy.py", "boto", "yea"]

# OPTION 4 - real PyTrim code

# install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install cython
RUN python3 -m pip install -r /tmp/requirements.txt

# FROM python:3.11-alpine
# FROM --platform=linux/amd64 python:3.11-alpine
# FROM --platform=${PYTRIM_BUILD_PLATFORM} python:3.11-alpine
# COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# was getting errors around libstc++ when doing "import pandas";
# this fixed it? https://github.com/bitwalker/alpine-erlang/issues/13. Similarly got errors about geos, libproj, etc.
# RUN apk update
# RUN apk --no-cache --update add libgcc libstdc++
# RUN apk --no-cache --update add geos-dev
# RUN apk --no-cache --update add proj

# copy Trim source code in
COPY temp/ /tmp/pytrim_src/

# A) install bash and let us peek around by attaching
# RUN apk add --no-cache bash
# CMD ["bash"]

# B) or, run the actual PyTrim simulator code and quit when done
CMD ["python3", "/tmp/pytrim_src/docker_entrypoint.py" ]
