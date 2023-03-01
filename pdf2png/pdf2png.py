import argparse, os
import pdf2image

#
def init():
	# retrieve output from arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--png_folder", type=str)
	args, _ = parser.parse_known_args()
	global png_folder_path
	png_folder_path = args.png_folder

#
def run(mini_batch):
	results = []
	for pdf_file in mini_batch:
		print(f"Converting {pdf_file} to PNG")
		images = pdf2image.convert_from_path(pdf_file)
		for i, image in enumerate(images):
			png_file_name = os.path.basename(pdf_file).replace(".pdf", f"_{i}.png")
			image.save(os.path.join(png_folder_path, png_file_name), "PNG")
			results.append(png_file_name)
	return results