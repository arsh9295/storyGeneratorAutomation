
import subprocess
import threading
import uuid
from flask import Flask, render_template_string, request, jsonify


app = Flask(__name__)

# Store job logs and progress
jobs = {}

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Run main.py</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 500px; margin: auto; }
        label, input, button { display: block; margin: 10px 0; }
        #progress-bar { width: 100%; background: #eee; border-radius: 5px; margin: 10px 0; }
        #progress { width: 0%; height: 20px; background: #4caf50; border-radius: 5px; }
        #log {
            background: #222;
            color: #eee;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            font-family: monospace;
            width: 80vw;
            max-width: 80vw;
            margin-left: -10vw;
            position: relative;
            left: -10vw;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Run main.py Multiple Times</h2>
        <form id="run-form">
            <label for="count">Number of times to run main.py:</label>
            <input type="number" id="count" name="count" min="1" value="1" required>
            <label for="filepath">File path (inside container, e.g. /app/configs/globalVariables.py):</label>
            <input type="text" id="filepath" name="filepath" required>
            <button type="submit">Start</button>
        </form>
        <div id="progress-bar"><div id="progress"></div></div>
        <h3>Live Log:</h3>
        <pre id="log"></pre>
    </div>
    <script>
    const form = document.getElementById('run-form');
    const progress = document.getElementById('progress');
    const log = document.getElementById('log');
    let jobId = null;
    let pollInterval = null;

    form.onsubmit = function(e) {
        e.preventDefault();
        log.textContent = '';
        progress.style.width = '0%';
        fetch('/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                count: form.count.value,
                filepath: form.filepath.value
            })
        })
        .then(r => r.json())
        .then(data => {
            jobId = data.job_id;
            pollInterval = setInterval(pollLog, 1000);
        });
    };

    function pollLog() {
        fetch('/progress/' + jobId)
        .then(r => r.json())
        .then(data => {
            log.textContent = data.log;
            progress.style.width = data.progress + '%';
            if (data.done) {
                clearInterval(pollInterval);
            }
        });
    }
    </script>
</body>
</html>
'''


@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML)

def run_job(job_id, count, filepath):
    jobs[job_id] = {'log': '', 'progress': 0, 'done': False}
    for i in range(count):
        jobs[job_id]['log'] += f'Run {i+1} starting...\n'
        try:
            process = subprocess.Popen(['python3', 'main.py', filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                jobs[job_id]['log'] += line
        except Exception as e:
            jobs[job_id]['log'] += f'Run {i+1} failed: {str(e)}\n'
        jobs[job_id]['progress'] = int(((i+1)/count)*100)
    jobs[job_id]['done'] = True

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    count = int(data['count'])
    filepath = data['filepath']
    job_id = str(uuid.uuid4())
    thread = threading.Thread(target=run_job, args=(job_id, count, filepath))
    thread.start()
    return jsonify({'job_id': job_id})

@app.route('/progress/<job_id>')
def progress(job_id):
    job = jobs.get(job_id, None)
    if not job:
        return jsonify({'log': 'No such job', 'progress': 0, 'done': True})
    return jsonify({'log': job['log'], 'progress': job['progress'], 'done': job['done']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
