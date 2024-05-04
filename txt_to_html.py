from xml.etree import ElementTree as ET
from argparse import ArgumentParser
import os

class colour:
  """
  Holds definitions for several colours to output in the terminal
  """
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def create_root(name: str) -> ET.Element:
  root = ET.Element("html")

  # Create head and body elements=
  head = ET.SubElement(root, "head")
  title = ET.SubElement(head, "title")
  title.text = name
  body = ET.SubElement(root, "body")
  h1 = ET.SubElement(body, "h1")
  h1.text = name
  
  style = ET.SubElement(head, "style")
  style.text = """
    body {
      background: linear-gradient(to bottom right, #CCCCFF, #9999FF);
      font-family: Verdana, Arial;
    }
    section {
      background-color: #fafafa;
      border: 2px solid #6699FF;
      border-radius: 25px;
      margin: 8px;
      padding: 0px 8px 0px 8px;
    }
    .shaded {
      background-color: #CCFFFF;
      border-radius: 25px;
      margin: 8px 0px 8px 0px;
      padding: 4px 8px 4px 8px;
    }
  """
  
  return root

def txt_to_html(input_file: str, root: ET.Element) -> ET.Element:
  """
  Converts a text file with header and paragraph to an HTML contents.
  Make necessary changes for multiple news articles. This script is
  only for one news article. Returns the updated root.

  Args:
      input_file (str): Path to the input TXT file.
      root (ET.Element): Root element to attach subelements
  """
  # Read text file content
  with open(input_file, 'r') as f:
    content = f.readlines()

  # Extract header and paragraph, since you will be having multiple articles the logic will
  # change for the code given below. 
  header = content[0].strip()
  paragraph = "".join(content[1:]).strip()

  # grab body from root
  body = root.find('.//body')

  # Create header and paragraph elements in body
  section = ET.SubElement(body, "section")
  h2 = ET.SubElement(section, "h2")
  h2.text = header
  p = ET.SubElement(section, "p")
  p.text = paragraph
  
  h2.set("class", "shaded")
  
  return root

def write_html_file(output_file: str, root: ET.Element) -> None:
  """
  Opens and attaches content to output file

  Args:
      output_file (str): Path to the output HTML file.
      root (ET.Element): Root element to that contains subelements
  """
  # Write HTML tree to file
  with open(output_file, 'wb') as f:
    tree = ET.ElementTree(root)
    tree.write(f, encoding='utf-8')
    
def open_file(file: str) -> None:
  try:
    os.startfile(file)  # Opens the file with the default application
  except AttributeError:
    try:
      # not Windows
      import subprocess
      subprocess.call(['open', file])
    except:
      print(f"{colour.FAIL}Could not open the file '{file}'.{colour.ENDC}")

def ParseArguments() -> tuple[str, str, int]:
  """
  Parses command line arguments
  """
  parser = ArgumentParser()
  parser.add_argument(help="Input TXT file base name. If using multiple input files, do not include the number at the end.", dest="base_input", type=str)
  parser.add_argument("--output", "-o", help="Output file path", dest="output_path", type=str, default="output.html")
  parser.add_argument("--count", "-c", help="Number of files to process. If using multiple input files, do not include the number at the end.", dest="count", type=int, default="1")
  args = parser.parse_args()
  baseInput = args.base_input
  outputPath = args.output_path
  count = args.count

  # clean up outputPath
  outputType = os.path.splitext(outputPath)[-1].lower()
  if (outputType == ""):
    outputPath += ".html"
    print(colour.WARNING + "Normalising input by adding .html extension..." + colour.ENDC)
  elif (outputType != ".html"):
    print(colour.WARNING + "Unexpected file type " + outputType + ". Proceed with caution." + colour.ENDC)

  #clean up baseInput
  inputType = os.path.splitext(baseInput)[-1].lower()
  if (inputType != ""):
    print(colour.WARNING + "Stripping input extension " + inputType + "..." + colour.ENDC)
    baseInput = os.path.splitext(baseInput)[0].lower()
      
  return (baseInput, outputPath, count)

def main() -> None:
  baseInput, outputPath, count = ParseArguments()
    
  print(colour.BOLD + "Creating HTML page..." + colour.ENDC)
  print(baseInput, outputPath, count)
  
  if count <= 1:
    root: ET.Element = create_root("The Onion Summary")
    root = txt_to_html(baseInput + ".txt", root)
  else:
    root: ET.Element = create_root("The Onion Summaries")
    for i in range(count):
      root = txt_to_html(baseInput + str(i) + ".txt", root)

  write_html_file(outputPath, root)

  print(colour.BOLD + colour.OKCYAN + "Success!" + colour.ENDC)
  print(f"{colour.BOLD}Converted text file '{baseInput}' to HTML file '{outputPath}'.{colour.ENDC}")
  
  open_file(outputPath)

if __name__ == "__main__":
    main()
