FROM python:3.10-slim AS base

ENV VIRTUAL_ENV=/opt/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV

WORKDIR /opt/app

COPY pip.conf /opt/env/pip.conf

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel -r requirements.txt && \
    rm /opt/env/pip.conf


FROM base AS dev

COPY requirements.dev.txt .
RUN pip install -r requirements.dev.txt

ENV PYTHONPATH=/opt/app/src
COPY . .

# While developing we should use pip install -e , but Docker does not support volumes during build,
# we would not get (*.egg-info) in the source code. That's why we install it normally,
# and after successfull built, we execute pip install -e on a running container.
RUN pip install -e .



FROM python:3.10-slim AS base

ENV VIRTUAL_ENV=/opt/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel -r requirements.txt && rm -rf ~/.cache


FROM base AS dev

COPY ./requirements-dev.txt ./requirements-dev.txt
COPY ./setup.py ./setup.py
COPY ./src ./src

RUN pip install -r requirements-dev.txt -e . && rm -rf ~/.cache


FROM base AS prod_build

COPY ./setup.py ./setup.py
COPY ./src ./src

RUN pip install . && rm -rf ~/.cache

FROM python:3.10-slim AS prod

ENV VIRTUAL_ENV=/opt/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=prod_build /opt/env /opt/env
CMD ["pip", "list"]
