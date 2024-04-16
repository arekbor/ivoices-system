#!/bin/bash

echo "API is running in dev environment. Every change refresh API..."

uvicorn app.main:app --reload