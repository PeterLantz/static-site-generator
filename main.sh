python3 src/main.py
echo "visit your site using this link - http://localhost:8888"
echo "quit server by using ctrl + C twice"
cd docs && python3 -m http.server 8888
cd ..
