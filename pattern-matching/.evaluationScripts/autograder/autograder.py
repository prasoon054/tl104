import json
import os
import subprocess
import sys
import tempfile

STUDENT_FILE = '/home/labDirectory/script.js'
OUTPUT_JSON = '/home/.evaluationScripts/evaluate.json'

TESTS = [
    ("abc123", True),
    ("a1", True),
    ("hello12345", True),
    ("123abc", False),
    ("abc", False),
    ("ABC123", False),
    ("abc123def", False),
    ("abc123!", False),
    ("", False)
]

NODE_RUNNER_SOURCE = r"""
const fs = require('fs');
const vm = require('vm');

const args = process.argv.slice(2);
if (args.length < 2) {
    console.error(JSON.stringify({__error__: "Usage: node runner.js <script.js> <json_tests_array>" }));
    process.exit(2);
}
const path = args[0];
let tests;
try {
    tests = JSON.parse(args[1]);
} catch (e) {
    console.error(JSON.stringify({__error__: "Cannot parse tests JSON: " + e.toString()}));
    process.exit(2);
}

try {
    const code = fs.readFileSync(path, 'utf8');
    const context = { console: console };
    vm.createContext(context);
    vm.runInContext(code, context);
    const out = [];
    for (let t of tests) {
        try {
            if (typeof context.validString !== 'function') {
                out.push({ input: t, error: 'validString is not defined or not a function' });
                continue;
            }
            const r = context.validString(t);
            // convert to boolean (in case user returns non-boolean)
            out.push({ input: t, valid: !!r });
        } catch (e) {
            out.push({ input: t, error: e && e.toString ? e.toString() : String(e) });
        }
    }
    console.log(JSON.stringify({__results__: out}));
} catch (e) {
    console.error(JSON.stringify({__error__: e && e.toString ? e.toString() : String(e) }));
    process.exit(1);
}
"""

def write_output(payload):
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=4)

def main():
    results = []
    total_score = 0
    max_score = len(TESTS)

    if not os.path.exists(STUDENT_FILE):
        payload = {
            'data': [],
            'total_score': 0,
            'maximum_score': max_score,
            'error': f"Student file not found at {STUDENT_FILE}"
        }
        write_output(payload)
        print("Student file not found. Wrote failure JSON.")
        return

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.js') as tr:
        tr.write(NODE_RUNNER_SOURCE)
        runner_path = tr.name

    try:
        tests_list = list(TESTS.keys())
        proc = subprocess.run(
            ['node', runner_path, STUDENT_FILE, json.dumps(tests_list)],
            capture_output=True, text=True, timeout=10
        )
    except FileNotFoundError:
        payload = {
            'data': [],
            'total_score': 0,
            'maximum_score': max_score,
            'error': "node.js executable not found. Install nodejs and npm in the lab environment."
        }
        write_output(payload)
        print("node not found. Wrote failure JSON.")
        return
    except subprocess.TimeoutExpired:
        payload = {
            'data': [],
            'total_score': 0,
            'maximum_score': max_score,
            'error': "Execution timed out."
        }
        write_output(payload)
        print("Execution timed out. Wrote failure JSON.")
        return
    finally:
        try:
            os.remove(runner_path)
        except Exception:
            pass

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    runner_output = None
    if stdout:
        try:
            parsed = json.loads(stdout)
            runner_output = parsed.get('__results__') or []
        except Exception:
            pass

    if not runner_output:
        try:
            parsed_err = json.loads(stderr) if stderr else {}
            if parsed_err and '__error__' in parsed_err:
                payload = {
                    'data': [],
                    'total_score': 0,
                    'maximum_score': max_score,
                    'error': parsed_err['__error__'],
                    'debug_stderr': stderr
                }
                write_output(payload)
                print("Runner returned error. Wrote failure JSON.")
                return
        except Exception:
            pass

        payload = {
            'data': [],
            'total_score': 0,
            'maximum_score': max_score,
            'error': "Could not parse node runner output.",
            'debug_stdout': stdout,
            'debug_stderr': stderr
        }
        write_output(payload)
        print("Could not parse runner output. Wrote failure JSON.")
        return

    # Evaluate each test
    total_score = 0
    data = []
    for entry in runner_output:
        input_val = entry.get('input')
        expected = TESTS.get(input_val, False)
        if 'error' in entry:
            score = 0
            status = 'failure'
            message = f"Error when executing validString('{input_val}'): {entry.get('error')}"
        else:
            got = bool(entry.get('valid', False))
            score = 1 if got == expected else 0
            status = 'success' if score == 1 else 'failure'
            message = (f"validString('{input_val}') returned {got}, expected {expected}")
        total_score += score
        data.append({
            'testid': f"validstring-{str(input_val) if input_val != '' else 'empty'}",
            'status': status,
            'score': score,
            'maximum marks': 1,
            'message': message
        })

    payload = {
        'data': data,
        'total_score': total_score,
        'maximum_score': max_score
    }
    write_output(payload)
    print(f"Evaluation finished. Score {total_score}/{max_score}. Output written to {OUTPUT_JSON}")

if __name__ == '__main__':
    main()
