from xml.etree import ElementTree
from io import BytesIO
import json

clinical_file = "combined-doctors-nurses-all-lower-clean.txt"



class ClinicalFile(object):
    def __init__(self, filename):
        self.f = open(filename)

    def read(self, size=None):
        line = self.f.readline()
        line_list = line.split(' ')
        new_list = []
        for i, item in enumerate(line_list):
            if i == 0:
                new_list.append(item)
                continue
            elif i == len(line_list) - 1:
                new_list.append(item)
                continue
            elif item == "&":
                new_item = item.replace('&', '&amp;')
                new_list.append(new_item)
            elif item == "<":
                new_item = item.replace('<', '&lt;')
                new_list.append(new_item)
            elif item == ">":
                new_item = item.replace('>', '&gt;')
                new_list.append(new_item)
            else:
                new_item = item.replace('"', '&quot;')
                new_list.append(new_item)
               
        

        new_line = " ".join(new_list)
        return new_line


for event, elem in ElementTree.iterparse(ClinicalFile(clinical_file), events=('start', 'end')):
    if event == "end":
        if elem.tag == "episode":
            episode_text = ""
            episode_summary = ""
            documents = elem.findall("document")
            for document in documents:
                doc_type = document.find("doc_type").text
                doc_type = doc_type.strip()
                # this is summary
                if doc_type == "dischargeEnd":
                    summary_sentences = document.findall("*//s")
                    for summary_sentence in summary_sentences:
                        episode_summary += "<s>" + summary_sentence.text + "</s> "
                elif doc_type == "dischargeMiddle":
                    continue
                # this is normal text
                else:
                    sentences = document.findall("*//s")
                    for sentence in sentences:
                        episode_text += sentence.text
            
            episode_data = {}
            episode_data["episode_text"] = episode_text
            episode_data["episode_summary"] = episode_summary
            episode_json = json.dumps(episode_data)
            print(episode_json)
            print()
            



