from minecraft_properties_editor import edit_file
from time import time
file = "server.properties"
start_ = time()
if __name__ == "__main__":
	x_ = edit_file(file=file, startx=start_, verbose=True).start()