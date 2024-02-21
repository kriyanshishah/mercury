# have node14 environment for creating custom frontend
which node
cd ../frontend
rm -rf build && yarn build
rm -rf ../mercury/frontend-dist
cd ../ 
rm -rf build/* dist/*
python3.9 setup.py bdist_wheel