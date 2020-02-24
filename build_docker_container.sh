#!/usr/bin/env bash

docker run --rm -i hadolint/hadolint < Dockerfile \
&& docker build . -t cooley.tech:build
