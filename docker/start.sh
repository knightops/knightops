#!/bin/bash

# 获取当前文件所在目录
basepath=$(cd `dirname $0`; pwd)
cd $basepath
cd ../

uvicorn server:app --host  0.0.0.0 --port 3060 --workers 2
