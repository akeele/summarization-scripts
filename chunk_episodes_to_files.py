import json
import argparse


argparser = argparse.ArgumentParser(description="Process care episodes json to their own files")
argparser.add_argument("--json", default=None, help="JSON file to process")
argparser.add_argument("--outdir", default=None, help="Directory for the output files")
args = argparser.parse_args()

with open(args.json, "r") as json_file:
    for idx, line in enumerate(json_file):
        line = line.strip()
        if len(line) == 0:
            continue
        episode_dict = json.loads(line)
        episode_text = episode_dict["episode_text"]
        episode_summary = episode_dict["episode_summary"]
        # ignore episodes without summaries
        if episode_summary == "":
            continue
        # write care episode to its own file
        with open(args.outdir+"care_episode"+str(idx)+".txt", "wt") as out_file:
            out_file.write(episode_text+"\n")
            out_file.write("@summary\n")
            out_file.write(episode_summary+"\n")
        
