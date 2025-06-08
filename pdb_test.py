from pybricks.hubs import PrimeHub
from pybricks.parameters import Button
from pybricks.tools import wait

hub = PrimeHub()

CHARS = (
    [chr(i) for i in range(ord('A'), ord('Z') + 1)] +
    [chr(i) for i in range(ord('0'), ord('9') + 1)] +
    [' ', '<', '↵']  # Space, Backspace, Enter
)
CHAR_BACKSPACE = '<'
CHAR_ENTER = '↵'

# Accepts ONLY positional arguments, ignores any extras
def hub_input(prompt="CMD:", _a=None, _b=None, _c=None, _d=None, _e=None, _f=None, _g=None, _h=None, _i=None, _j=None, _k=None, _l=None, _m=None, _n=None, _o=None, _p=None, *ignore):
    idx = 0
    cmd = ""
    editing = True

    # Only use the first argument as prompt, ignore the rest
    print(prompt, end="", flush=True)
    hub.display.char(CHARS[idx % len(CHARS)])

    while editing:
        while not hub.buttons.pressed():
            wait(10)
        pressed = hub.buttons.pressed()

        if Button.LEFT in pressed:
            idx = (idx - 1) % len(CHARS)
            hub.display.char(CHARS[idx % len(CHARS)])
            while Button.LEFT in hub.buttons.pressed():
                wait(10)

        elif Button.RIGHT in pressed:
            idx = (idx + 1) % len(CHARS)
            hub.display.char(CHARS[idx % len(CHARS)])
            while Button.RIGHT in hub.buttons.pressed():
                wait(10)

        elif Button.CENTER in pressed:
            c = CHARS[idx % len(CHARS)]
            if c == CHAR_ENTER:
                editing = False
            elif c == CHAR_BACKSPACE:
                if len(cmd) > 0:
                    cmd = cmd[:-1]
            else:
                cmd += c
            print("Currently typing:", cmd)
            if cmd:
                hub.display.char(cmd[-1])
            else:
                hub.display.char(' ')
            wait(200)
            while Button.CENTER in hub.buttons.pressed():
                wait(10)

        while hub.buttons.pressed():
            wait(10)

    print("\nTyped command:", cmd)
    hub.display.clear()
    return cmd

class MicroPdb:
    def __init__(self):
        self.active = True

    def set_trace(self, local_vars=None, global_vars=None):
        print("\n-- MicroPython PDB (Hub Input, PC Output) --")
        print("Type variable names, 'c' to continue, 'l' for locals, 'll' for long list, or any Python expression.")
        while self.active:
            print("send command:")
            # Call with only one positional argument
            cmd = hub_input("CMD:")
            if cmd is None:
                print("Debugger exited by user.")
                break
            cmd = cmd.strip()
            print("(mpdb) " + cmd)
            if cmd in ('c', 'continue'):
                print("Continuing execution.")
                break
            elif cmd in ('q', 'quit'):
                print("Debugger quit.")
                self.active = False
                break
            elif cmd in ('l', 'locals'):
                print("Locals:")
                for k, v in (local_vars or {}).items():
                    print("  {} = {!r}".format(k, v))
            elif cmd == 'll':
                print("long list executed")
            elif cmd:
                try:
                    if local_vars and cmd in local_vars:
                        print(repr(local_vars[cmd]))
                    elif global_vars and cmd in global_vars:
                        print(repr(global_vars[cmd]))
                    else:
                        print(repr(eval(cmd, global_vars, local_vars)))
                except Exception as e:
                    print("Error:", e)

_debugger = MicroPdb()

def breakpoint(local_vars=None, global_vars=None):
    _debugger.set_trace(local_vars, global_vars)

# Example usage
if __name__ == "__main__":
    def test():
        a = 123
        b = "hello"
        breakpoint(locals(), globals())
        print("After breakpoint", a, b)
    test()
