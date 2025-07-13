import re
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

from dividedpkg import PKG, xor_parallel, get_key
from dividedpkg.patch_exe import patch_exe, PatchError

def apply(folder: str|Path):
	folder = Path(folder)
	if folder.suffix:
		folder = folder.parent
	
	if folder.stem == "pkgs":
		exe = folder.parent / "Indivisible.exe"
		pkgs = folder
	else:
		exe = folder / "Indivisible.exe"
		pkgs = folder / "pkgs"
	
	try:
		patch_exe(exe)
	except PatchError as err:
		print(err, file=sys.stderr)
		return 1

	## Swap buttons as they appear in text
	print("Swapping buttons outside of battle...")
	data1 = pkgs / "data_1.pkg"
	data = bytearray(data1.read_bytes())
	xor_parallel(data, get_key(), 0)

	def switch(mo: re.Match):
		return {
			b"A": b"B", b"B": b"A",
			b"X": b"Y", b"Y": b"X",
		}[mo.group(1)]
	re.sub(br"\{X([ABXY])\}", switch, data)
	xor_parallel(data, get_key(), 0)
	data1.write_bytes(data)
	print(" ...swapped")

	## Swap buttons as they appear in battle
	print("Swapping buttons in battle...")
	data8 = PKG.load(pkgs / "data_8.pkg")
	filekey = "lz4/UI/Win/Textures/TA_1000_1.dds.lz4"
	dds = data8.read(filekey)
	img = Image.open(BytesIO(dds))
	# All buttons at Y 1232
	# Layout of A B X Y A B X Y starting at 1370
	# Each button is 49x49 (rounding to 50) and
	# are 62 pixels from left side to left side
	button = [
		(box, img.crop(box))
		for x in range(1370, 1850, 62)
		for box in [(x, 1232, x+50, 1282)]
	]

	for i in range(0, 8, 2):
		img.paste(button[i+1][1], button[i+0][0])
		img.paste(button[i+0][1], button[i+1][0])
	dds_out = pkgs / "data_8" / filekey.removesuffix(".lz4")
	out = dds_out.with_suffix(".png")
	img.save(out)
	p = subprocess.run(
		["nvcompress.exe", "-bc3", "-srgb", str(out), str(dds_out)],
		cwd=Path(__file__).parent
	)
	if p.returncode != 0:
		print("could not convert DDS", file=sys.stderr)
		return 2

	data8.import1(filekey, pkgs / "data_8")
	print(" ...swapped")
	return 0


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} path\\to\\Indivisible")
		sys.exit(0)
	sys.exit(apply(sys.argv[1]))
