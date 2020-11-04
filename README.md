# stable-mango

Chart.js from `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js`

JQuery from `https://code.jquery.com/jquery-3.5.1.min.js`

Setup:

```bash
python3 -m pip install -r requirements.txt
```

To run:

```bash
python3 poll.py &
export FLASK_APP=main.py
python3 -m flask run --port=42069 --host=0.0.0.0
```