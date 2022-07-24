from sys import stdout
from time import time
from re import search, match
class open_file():
	global stdout
	@staticmethod
	def verbose_output(verbose_level:bool, msg:str):
		if verbose_level == True:
			stdout.write(msg + "\r\x0A")
	def __init__(self):
		open_file.verbose_output(self.verbose, "[VERBOSE] Reading file :: %s!"%(self.file))
		self.file = b"\r\x0A".join(bob for bob in open(self.file, "rb")) # CRLF included.
		open_file.verbose_output(self.verbose, "[VERBOSE] Read %d-bytes!"%(len(self.file)))
	def start(self):
		self.file = self.file.decode("utf-8", errors="ignore")
		self.run_context()
class edit_file(open_file):
	global search, match, time, stdout
	def __init__(self, file:str,startx:float, verbose=False) -> str:
		self.file = file
		self.dir_ = file
		self.startx = startx
		self.verbose = verbose
		open_file.__init__(self)
	def run_context(self):
		def check(actual:str, action:str) -> str:
			casers = {"motd":[r"[ A-Za-z]", "string, str, text"]}
			if action in casers and search(casers[action][0], actual) == None:
				return False, casers[action][1]
			return True, "nothing"
		loaded = {}
		open_file.verbose_output(self.verbose, "[VERBOSE] Preparing to parse lines. . .!\r\x0A")
		for nm, items in enumerate(self.file.split("\r\x0A"), 0):
			if "#" not in items and items != "":
				var, value = items.split("=")
				loaded[var] = value
				open_file.verbose_output(self.verbose, "[VERBOSE] %s -> %s #%d!"%(var, value, nm))
		print("\n"*100)
		action = {}
		for nm, values in enumerate(loaded, 1):
			action[nm] = values
		print(">> Choose an option. . .[CTRL-Z -> break]")
		actuals = "\r\x0A".join("%d. %s"%(nm, bob) for nm, bob in enumerate(loaded, 1))
		print(actuals + "\r\x0A" + "\x2D"*40 + "\r\x0A")
		changed = 0
		while True:
			try:
				inp = input("option[1-%d]>> "%(len(action)))
			except KeyboardInterrupt:
				break
			try:
				inp = int(inp)
			except:
				print("non int value provided!")
				continue
			if inp not in action:
				continue
			actual = input("[DATA] Value for %s: "%(action[int(inp)]))
			if actual in ["False", "True"]:
				actual = actual.lower()
			ans, tp = check(actual, action[int(inp)])
			if ans == False:
				print("incorrect type, required: %s"%(tp))
			loaded[action[int(inp)]] = actual
			changed += 1
		print("[DATA] Total changed: %d!\r\x0A")
		with open(self.dir_, "wb") as file:
			file.write(("\r\x0A".join(bob + "=" + loaded[bob] for bob in loaded)).encode("utf-8", errors='ignore'))
		file.close()
		print("[DATA] Writing finished!\r\x0A\r\x0A")
		end = time() - self.startx
		print("ended with total time (after execution): %ss!"%(int(end)))
