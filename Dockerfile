# base image
FROM python:3.7.2-slim

ARG APP_HOME=/opt/app

# install required libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat \
    curl \
    && apt-get clean

# install node
WORKDIR /opt
RUN curl -sL https://deb.nodesource.com/setup_11.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh

# install Node.js 11.x and npm
RUN apt-get install -y \
    nodejs

# create user and group both named `user`
RUN groupadd -r user && useradd --create-home -r -g user user
RUN mkdir -p $APP_HOME && chown -R user:user $APP_HOME
USER user

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH "/home/user/.poetry/bin:${PATH}"

# set working directory
WORKDIR $APP_HOME

# add and install js requirements
COPY package.json .
COPY package-lock.json .
RUN npm install

# add and install python requirements
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# bake code in
COPY . $APP_HOME

# run server
CMD ["poetry", "run", "python", "run.py"]
