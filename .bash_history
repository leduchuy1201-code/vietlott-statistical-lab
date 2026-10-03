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
git add .
git commit -m "Phiên bản hoàn thiện: Giao diện và API"
gh auth login
gh repo create vietlott-statistical-lab --public --source=. --remote=origin --push
git branch -M main
git push -u origin main --force
git rm -r --cached firebase_credentials.json
git rm -r --cached .codeoss/
git rm -r --cached .cache/
echo "firebase_credentials.json" >> .gitignore
echo ".codeoss/" >> .gitignore
echo ".cache/" >> .gitignore
git add .gitignore
git commit --amend --no-edit
git push -u origin main --force
pip install scikit-learn pandas
touch core/ml_engine.py test_ml.py
python3 test_ml.py
git add .
git commit -m "Tích hợp AI Random Forest vào giao diện"
git push -u origin main
git push -u origin main --force
git rm -r --cached .config/
echo ".config/" >> .gitignore
git add .gitignore
git commit --amend --no-edit
git push -u origin main --force
git add requirements.txt
git commit -m "Bổ sung thư viện AI cho máy chủ"
git push -u origin main
git add app.py
git commit -m "Sửa lỗi thiếu dấu phẩy ở app.py"
git push -u origin main
git add app.py
git commit -m "Sửa lỗi thiếu dấu phẩy ở app.py lần 2"
git push -u origin main
git add app.py
git commit -m "Sửa lỗi thiếu import db_manager"
git push -u origin main
git add templates/index.html
git commit -m "Sửa lỗi lặp bảng AI 5 lần"
git push -u origin main
git add templates/index.html
git commit -m "Cập nhật file HTML hoàn chỉnh"
git push -u origin main
touch test_max3d.py
python3 test_max3d.py
test_max3d.py
python3 test_max3d.py
touch test_ml_max3d.py
python3 test_ml_max3d.py
git add app.py
git commit -m "Thêm API hoàn chỉnh cho Max 3D"
git push -u origin main
git add templates/index.html
git commit -m "Cập nhật giao diện Đa trò chơi Mega & Max 3D"
git push -u origin main
git add templates/index.html
git commit -m "Cập nhật HTML với bộ quét lỗi chi tiết"
git push -u origin main
git add templates/index.html
git commit -m "Bọc áo giáp bắt lỗi JSON"
git push -u origin main
git add .
git commit -m "Đẩy toàn bộ Lõi AI và Collector của Max 3D lên máy chủ"
git push -u origin main
