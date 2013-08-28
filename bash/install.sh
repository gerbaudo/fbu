virtualenv .
source bin/activate
cat requirements.txt | xargs pip install
