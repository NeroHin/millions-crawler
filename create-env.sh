#!/bin/bash

# create .env file
touch .env

# insert content into .env file
echo "REDIS_HOST=" >> .env
echo "REDIS_PORT=" >> .env
echo "REDIS_PASSWORD=" >> .env
echo "MONGODB_URI=" >> .env
echo "MONGODB_DB_NAME=" >> .env
echo "MONGODB_USERNAME=" >> .env
echo "MONGODB_PASSWORD=" >> .env
