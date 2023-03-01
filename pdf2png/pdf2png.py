import argparse, os
import pandas as pd
import pdf2image

#
global png_folder_path

#
def init():
	# retrieve output from arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--png_folder", type=str)
	args, _ = parser.parse_known_args()
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
		results.append(pdf_file,'converted')
	return pd.DataFrame(results)

# local unit test
if __name__ == "__main__":
	pdf_folder_path = 'datalake/pdf'
	png_folder_path = 'datalake/png'
	# list all files in png_folder_path
	pdf_files = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith(".pdf")]
	print(run(pdf_files))