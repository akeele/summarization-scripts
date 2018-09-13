#from sumy.summarizers.lsa import LsaSummarizer
#from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from lex_rank_summarizer import LexRankSummarizer
from lsa_summarizer import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
from sumy.evaluation.rouge import rouge_n
from numpy.linalg.linalg import LinAlgError
import json

from datetime import datetime

startTime = datetime.now()




LANGUAGE = "finnish"
SENTENCE_COUNT = 20
summarizer = LsaSummarizer() # Define summarization method you want to use
summarizer.stop_words = get_stop_words(LANGUAGE)
tokenizer = Tokenizer(LANGUAGE)

counter = 0
rouge_1_total = 0
rouge_2_total = 0
reference_summary_count = 0
with open("/home/a/akeele/summarization-data/combined-doctors-nurses-all-lower-text.json", "r") as data:

    for line in data:
        if len(line.strip()) == 0:
            continue
        json_data = json.loads(line)
        counter += 1
        episode_text = json_data["episode_text"]
        episode_summary = json_data["episode_summary"]
        # read the reference summary
        reference_summary = PlaintextParser.from_string(episode_summary, tokenizer)
        reference_sentences = reference_summary.document.sentences
        # read the episode text
        parser = PlaintextParser.from_string(episode_text, tokenizer)
        # Needed for LSA
        try:
            evaluated_sentences = summarizer(parser.document, SENTENCE_COUNT)
        except LinAlgError:
            continue
        try:
            rouge_1 = rouge_n(evaluated_sentences, reference_sentences, 1)
        except ValueError:
            print("Reference summary not available for this episode")
            print()
            continue
        rouge_2 = rouge_n(evaluated_sentences, reference_sentences, 2)
        rouge_1_total += rouge_1
        rouge_2_total += rouge_2
        reference_summary_count += 1
        
        for sentence in summarizer(parser.document, SENTENCE_COUNT):
            print(sentence)
        print()
        print("Rouge-1: ", rouge_1)
        print("Rouge-2: ", rouge_2)
        print()
        #if counter > 100:
         #   break

print("ROUGE-1 avg: ", rouge_1_total/reference_summary_count)
print("ROUGE-2 avg: ", rouge_2_total/reference_summary_count)

print("Time: ", datetime.now() - startTime)
