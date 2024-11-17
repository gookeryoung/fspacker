pub const INIT_SCRIPT: &str = r#"
import sys\n
import os\n
import copy\n
import site\n

FSPLOADER = os.environ['FSPLOADER']\n
FSPLOADER_HOME = os.environ['FSPLOADER_HOME']\n
FSPLOADER_RUNTIME = os.environ['FSPLOADER_RUNTIME']\n
FSPLOADER_SCRIPT = os.environ['FSPLOADER_SCRIPT']\n

sys.path_origin = [n for n in sys.path]\n
sys.FSPLOADER = FSPLOADER\n
sys.FSPLOADER_HOME = FSPLOADER_HOME\n
sys.FSPLOADER_SCRIPT = FSPLOADER_SCRIPT\n

def MessageBox(msg, info = 'Message'):\n
    import ctypes\n
    ctypes.windll.user32.MessageBoxW(None, str(msg), str(info), 0)\n
    return 0\n

os.MessageBox = MessageBox\n

for n in ['.', 'lib', 'site-packages', 'runtime']:\n
    dir_ = os.path.abspath(os.path.join(FSPLOADER_HOME, n))\n
    if os.path.exists(dir_):\n
        site.addsitedir(dir_)\n

sys.argv = [FSPLOADER_SCRIPT] + sys.argv[1:]\n
text = open(FSPLOADER_SCRIPT, 'rb').read()\n

environ = {'__file__': FSPLOADER_SCRIPT, '__name__': '__main__'}\n
environ['__package__'] = None\n
code = compile(text, FSPLOADER_SCRIPT, 'exec')\n
exec(code, environ)\n
"#;
