#
import argparse, os

#
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# 
from dotenv import load_dotenv
load_dotenv()
COGNITIVE_SERVICES_ENDPOINT = os.getenv("COGNITIVE_SERVICES_ENDPOINT")
COGNITIVE_SERVICES_API_KEY = os.getenv("COGNITIVE_SERVICES_API_KEY")

#
def init():
	# retrieve output from arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--json_folder", type=str)
	args, _ = parser.parse_known_args()
	global json_folder_path
	json_folder_path = args.json_folder
	# init form recognizer client
	global document_analysis_client
	endpoint = "https://<my-custom-subdomain>.cognitiveservices.azure.com/"
	credential = AzureKeyCredential(COGNITIVE_SERVICES_API_KEY)
	document_analysis_client = DocumentAnalysisClient(COGNITIVE_SERVICES_ENDPOINT, credential)

#
def run(mini_batch):
	results = []
	for png_file in mini_batch:
		print(f"Converting {png_file} to JSON")
		with open(png_file, "rb") as png:
			document = png.read()
		poller = document_analysis_client.begin_analyze_document("prebuilt-document", document)
		result = poller.result()
		json_file_name = os.path.basename(png_file).replace(".png", ".json")
		with open(os.path.join(json_folder_path, json_file_name), "w") as json_file:
			json_file.write(result.serialize())
		results.append(json_file_name)
	return results