#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
  open UnityClient/neural-mmo.app
else
  ./UnityClient/neural-mmo.x86_64
fi
