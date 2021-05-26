import json
import boto3 
import urllib.request
import convo_parser

def lambda_handler(event, context):
    
    # 1. Set up Transcribe client
    transcribe = boto3.client('transcribe')
    
    # 2. Use client to call GetTranscriptionJob - check status of transcription
    job_name = event['queryStringParameters']['job_name']
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    
    # 3a. If transcription is completed, fetch transcript .json file
    if job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        
        # 4. Load content from transcript file, as json/dict
        # (urlopen returns a bytes-object)
        with urllib.request.urlopen(transcript_file_uri) as f:
            # load bytes as json
            transcript_json = json.load(f)

            convo_parse = True
            # 4.b If parsing into speaker paragraphs, run convo_parser script
            if convo_parse == True:
                transcript_text = convo_parser.parse_convo(transcript_json)
            else:
                transcript_text = transcript_json['results']['transcripts'][0]['transcript']
            
    # 3b. If transcription is not completed, set transcript text to INCOMPLETE
    else:
        transcript_text = 'INCOMPLETE'
            
    # 4. Construct response object with transcript_text and job status
    response_object = {
        'transcript_text': transcript_text,
        'status':  job['TranscriptionJob']['TranscriptionJobStatus']
        }
        
    # 5. Return results
    return {
        'statusCode': 200,
        'body': json.dumps(response_object)
    }