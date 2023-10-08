import sys
import subprocess
from string import Template

def _extract_response(stdout):
    response = []
    is_response = False
    for line in stdout:
        if is_response:
            response.append(line.decode())
        elif line.startswith(b'###Assistant:'):
            is_response = True

    return ''.join(response) if len(response) > 0 else None

def llm(prompt, *args):
    template = Template("###User:\n$prompt\n###Assistant:\n""")

    if not prompt:
        raise Exception("Prompt must be provided!")

    llm_args = [
        "./llm/mainbin", 
        "-m", "./llm/model/ggml-model-q5_K_M.gguf"
    ]

    if args:
        llm_args += args

    llm_args += ['-p', template.substitute(prompt=prompt)]
    popen = subprocess.Popen(llm_args, stdout=subprocess.PIPE)
    popen.wait()
    return _extract_response(popen.stdout)

if __name__ == '__main__':
    print('Response:', llm(sys.argv[-1], *sys.argv[1:-1]))
