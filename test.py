from contextlib import redirect_stdout
import io

f = io.StringIO()
with redirect_stdout(f):
    print("Wow")
s = f.getvalue()
print("just another print {}".format(s))
