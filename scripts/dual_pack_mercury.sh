#!/bin/bash

echo 'Dual Pack Mercury'

# clear dist directories
rm -rf mercury/frontend-dist
rm -rf mercury/frontend-single-site-dist

cd frontend
yarn install
yarn build

mv build/ ../mercury/frontend-dist

cd ..
rm mercury/*.sqlite*

python setup.py sdist bdist_wheel
