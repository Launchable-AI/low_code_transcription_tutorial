import json
import math

def parse_convo(transcript_json_data):
    # with open(filepath, 'r') as tmp_json_file:

        # 1. load transcript into memory
    # transcript_json_data = json.loads(transcript)

    # 2. set up some helper variables
    seg_index = 0
    items = transcript_json_data['results']['items']
    segments = transcript_json_data['results']['speaker_labels']['segments']

    # 3. seed each segment with an empty sentence
    for segment in segments:
        segment['sentence'] = ''

    # 4. iterate through 'items', adding each to appropriate segment's sentence
    for index, item in enumerate(items):
        item_content = item['alternatives'][0]['content']
        # 4.a parse punctutation
        # (i.e., add to current sentence; punctuation never marks the beginning of a new sentence)
        if item['type'] == 'punctuation':
            segments[seg_index]['sentence'] = segments[seg_index]['sentence'] + item_content
        elif item['type'] == 'pronunciation':
            # 4.b parse words
            # b.1. if on final segment, simply add word
            if seg_index == len(segments) - 1:
                segments[seg_index]['sentence'] = segments[seg_index]['sentence'] + ' ' + item_content
            # b.2. if not, check whether need new utterance added
            else:
                if float(item['end_time']) > float(segments[seg_index]['end_time']):
                    seg_index += 1
                # add current word to segment's 'sentence'
                segments[seg_index]['sentence'] = segments[seg_index]['sentence'] + ' ' + item_content

    # 5. Combine sentences from same speaker into paragraphs
    seg_start_time = 0  # keep track of start_time for first seg in utterance
    dict_convo = []
    for index,seg in enumerate(segments[:-2]):
        # if speaker is the same for contiguous segments, combine their sentences
        if segments[index]['speaker_label'] == segments[index+1]['speaker_label']:
            segments[index+1]['sentence'] = segments[index]['sentence'] + segments[index+1]['sentence']
        # if not, add combined sentence to dict_convo
        else:
            seg['start_time'] = seg_start_time
            dict_convo.append(seg)
            seg_start_time = segments[index+1]['start_time']

    # 5.b add last segment to dict_convo; it was processed above
    dict_convo.append(segments[-1])

    # 6. Replace default spk_0, spk_1, etc., with more human-readable labels
    # 6.a use dict to clean up speaker labels, more reader-friendly
    speakers_dict = {
        "spk_0": "Speaker1",
        "spk_1": "Speaker2",
        "spk_2": "Speaker3",
        "spk_3": "Speaker4",
        "spk_4": "Speaker5",
        "spk_5": "Speaker6",
        "spk_6": "Speaker7",
        "spk_7": "Speaker8",
        "spk_8": "Speaker9",
        "spk_9": "Speaker10"
        }

    # 6.b replace speaker labels
    for utterance in dict_convo:
        speaker = utterance['speaker_label']
        if speaker in speakers_dict.keys():
            utterance['speaker_label'] = speakers_dict[speaker]


    # 7. Convert dict representation of conversation to plain text representation
    text_convo = str()

    for seg in dict_convo:
        speaker_header = f'{seg["speaker_label"]}'
        start_time = math.floor(float(seg["start_time"]))
        end_time = math.floor(float(seg["end_time"]))
        time_header = f'{start_time}s - {end_time}s'
        sentence = f'{seg["sentence"]}'

        # compile each paragraph
        text_convo += f'{speaker_header}\t\t{time_header}\n{sentence}\n\n'

    print(text_convo)
    return text_convo

# parse_convo('./2speaker_transcript.json')
