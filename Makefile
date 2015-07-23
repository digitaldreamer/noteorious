ALL=poseidon postgres virtualenv
PROJECT=service
ROOT_DIR=~/www
ENVS_DIR=~/envs
PROJECT_DIR=$(ROOT_DIR)/$(PROJECT)
UNAME := $(shell uname) # detech os, not windows compliant

.PHONY: help less $(ALL)

help:
	cat $(PROJECT_DIR)/README.rst

all: $(ALL)

virtualenv:
	mkdir -p $(ENVS_DIR)
	cd $(ENVS_DIR); virtualenv $(PROJECT)
	. $(ENVS_DIR)/$(PROJECT)/bin/activate; pip install -Ur $(PROJECT_DIR)/requirements/requirements.txt

less: server
	sudo apt-get install -y nodejs
	cd ~/; npm install less jshint

server:
	sudo apt-get install -y openjdk-7-jdk
	sudo apt-get install -y python-software-properties
	sudo apt-get install -y nginx
	sudo apt-get install -y libffi-dev
	sudo apt-get install -y libpq-dev
	sudo apt-get install -y sqlite3
	# sudo apt-get install -y memcached
	sudo easy_install virtualenv

redis:
	sudo apt-get install -y redis-server

mongo:
	sudo apt-get install -y mongodb

postgres:
	sudo apt-get install -y libpq-dev
	sudo apt-get install -y postgresql
	sudo apt-get install -y python-psycopg2
