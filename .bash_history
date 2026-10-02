mkdir vietlott-statistical-lab
cd vietlott-statistical-lab
python3 --version
git init
echo "# Vietlott Statistical Lab" > README.md
touch hello.py
python3 hello.py
pip install firebase-admin
python3 hello.py
touch test_firestore.py
python3 test_firestore.py
mkdir core
touch core/__init__.py core/config.py test_config.py
python3 test_config.py
touch core/database.py test_db.py
python3 test_db.py
pip install requests beautifulsoup4
touch core/collector.py test_collector.py
python3 test_collector.py
pip install requests-html
python3 test_collector.py
pip install lxml_html_clean
python3 test_collector.py
python3 test_collector.pycurl -s https://api.github.com/repos/vietvudanh/vietlott-data/contents/data | grep '"name":'
curl -s https://api.github.com/repos/vietvudanh/vietlott-data/contents/data | grep '"name":'
python3 test_collector.py
touch core/statistics.py test_statistics.py
python3 test_statistics.py
touch test_real_statistics.py
python3 test_real_statistics.py
touch core/pipeline.py test_pipeline.py
python3 test_pipeline.py
pip install Flask
touch app.py
python3 app.py
mkdir templates
touch templates/index.html
python3 app.py
echo -e "Flask==3.0.0\nfirebase-admin==6.5.0\nrequests==2.31.0\ngunicorn==21.2.0" > requirements.txt
echo -e "__pycache__/\n*.pyc\n.idea/\n.vscode/" > .gitignore
git config --global user.name "Data Engineer"
git config --global user.email "data@engineer.com"
