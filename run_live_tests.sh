#!/usr/bin/env bash

SANDBOX_CLIENT_KEY='<your-client-key>'
SANDBOX_SERVER_KEY='<your-server-key'
RUN_ALL_ACCEPTANCE_TESTS=0 

export SANDBOX_CLIENT_KEY
export SANDBOX_SERVER_KEY
export RUN_ALL_ACCEPTANCE_TESTS

nosetests