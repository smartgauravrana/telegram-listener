Run command
python3 main.py# telegram-listener

server cmd
pm2 start main.py --interpreter python --name telegram-listener

## Steps to run on server:

1. Goto source code directory
2. python3 -m venv myenv
3. source myenv/bin/activate
4. pip install -r requirements.txt
5. pm2 start main.py --interpreter python --name telegram-listener
