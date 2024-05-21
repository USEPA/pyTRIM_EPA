# references; used these as tutorial plus a starting point, then made my own changes...
# https://docs.docker.com/get-started/02_our_app/
# https://simonwillison.net/2018/Nov/19/smaller-python-docker-images/

FROM python:3.11-alpine as builder

# Install all the python libraries we need to run...Alpine lacks a compiler toolchain for building some things we need, like pandas.
RUN apk add --no-cache gcc python3-dev musl-dev alpine-sdk

# START - some Python packages can't install/build via pip without some extra work.
# (pyproj)
RUN apk add proj proj-dev
RUN apk add proj-util

# (shapely)
RUN apk add geos geos-dev

# END - some Python packages..


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

FROM python:3.11-alpine
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# was getting errors around libstc++ when doing "import pandas";
# this fixed it? https://github.com/bitwalker/alpine-erlang/issues/13. Similarly got errors about geos, libproj, etc.
RUN apk update
RUN apk --no-cache --update add libgcc libstdc++
RUN apk --no-cache --update add geos-dev
RUN apk --no-cache --update add proj

# copy Trim source code in
COPY temp/ /tmp/pytrim_src/

# A) install bash and let us peek around by attaching
# RUN apk add --no-cache bash
# CMD ["bash"]

# B) or, run the actual PyTrim simulator code and quit when done
CMD ["python3", "/tmp/pytrim_src/docker_entrypoint.py" ]
