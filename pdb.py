# micropdb_minimal.py - Minimal MicroPython Debugger

class MicroPDB:
  def __init__(self):
    self.stepping = False
    self.quitting = False
    self.locals = {}
    self.globals = {}
    
  def set_trace(self, locals_dict=None, globals_dict=None):
    self.locals = locals_dict if locals_dict is not None else {}
    self.globals = globals_dict if globals_dict is not None else {}
    self.interaction()
    
  def interaction(self):
    print("\n--MICROPYTHON DEBUGGER--")
    
    while not self.quitting:
      try:
        command = input("(Mpdb) ")
        self.handle_command(command)
        
        if self.stepping or self.quitting:
          break
      except Exception as e:
        print(f"Error: {e}")
        
  def handle_command(self, cmd):
    cmd = cmd.strip()
    if not cmd:
      return
      
    parts = cmd.split(maxsplit=1)
    command = parts[0]
    args = parts[1] if len(parts) > 1 else ""
        
    # Command handlers
    if command in ('h', 'help'):
      self.do_help()
    elif command in ('q', 'quit'):
      self.do_quit()
    elif command in ('c', 'continue'):
      self.do_continue()
    elif command in ('n', 'next'):
      self.do_next()
    elif command in ('p',):
      self.do_print(args)
    elif command in ('l', 'locals'):
      self.do_locals()
    elif command.startswith('!'):
      self.do_execute(cmd[1:])
    else:
      try:
        value = eval(command, self.globals, self.locals)
        print(repr(value))
      except Exception as e:
        print(f"Unknown command or expression: {command}")
      
  def do_help(self):
    print("Available commands:")
    print("  h(elp)      - Show this help")
    print("  q(uit)      - Quit the debugger")
    print("  c(ontinue)  - Continue execution")
    print("  n(ext)      - Execute current line and stop at next line")
    print("  p expr      - Print value of expression")
    print("  l(ocals)    - List local variables")
    print("  !expr       - Execute Python expression in current context")
    
  def do_quit(self):
    self.quitting = True
    
  def do_continue(self):
    self.stepping = False
    
  def do_next(self):
    self.stepping = True
    
  def do_locals(self):
    print("Local variables:")
    for name, value in self.locals.items():
      print(f"  {name} = {repr(value)}")
      
  def do_print(self, arg):
    if not arg:
      print("Print requires an expression")
      return
      
    try:
      value = eval(arg, self.globals, self.locals)
      print(repr(value))
    except Exception as e:
      print(f"Error: {e}")
        
  def do_execute(self, expr):
    try:
      exec(expr, self.globals, self.locals)
    except Exception as e:
      print(f"Error: {e}")

# Create a global debugger instance
_debugger = MicroPDB()

# Function to create a breakpoint
def breakpoint():
  # Simple version that just captures the current scope
  _debugger.set_trace(locals(), globals())

# Alias for compatibility
set_trace = breakpoint

# Safe frame access function
def get_caller_frame():
  try:
    # Try using inspect if available
    try:
      import inspect
      frame = inspect.currentframe()
      if frame is not None and hasattr(frame, 'f_back'):
        return frame.f_back
    except ImportError:
      pass
      
    # Try using sys._getframe if available
    try:
      import sys
      if hasattr(sys, '_getframe'):
        frame = sys._getframe(1)  # Get caller's frame
        return frame
    except (ImportError, AttributeError):
      pass
      
    # Try using exception trick as last resort
    try:
      raise Exception()
    except:
      import sys
      tb = sys.exc_info()[2]
      if tb is not None and hasattr(tb, 'tb_frame') and hasattr(tb.tb_frame, 'f_back'):
        return tb.tb_frame.f_back
    
  except Exception:
    pass
    
  # If all methods fail, return None
  return None

# Enhanced breakpoint function that tries multiple methods
def breakpoint_enhanced():
  frame = get_caller_frame()
  if frame is not None:
    # We have a frame, use its locals and globals
    _debugger.set_trace(frame.f_locals, frame.f_globals)
  else:
    # Fallback to current scope
    _debugger.set_trace(locals(), globals())

# Use the enhanced version if available
try:
  # Test if we can get frame information
  test_frame = get_caller_frame()
  if test_frame is not None:
    # Frame access works, use enhanced version
    breakpoint = breakpoint_enhanced
except:
  # Stick with simple version
  pass
