import os
import sys
sys.path.insert(0, os.path.realpath(__file__).replace('run.py', '') + 'src')
import graphic as g

app = g.AndroidLoggingGUI()
app.mainloop()