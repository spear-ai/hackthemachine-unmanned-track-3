#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
  open model/client/UnityClient/neural-mmo.app
else
  ./model/client/UnityClient/neural-mmo.x86_64
fi
