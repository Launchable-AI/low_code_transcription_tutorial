import json
import boto3
import uuid

def lambda_handler(event, context):

    # 1. Create a trancsribe client for Transcribe
    transcribe = boto3.client('transcribe')
    
    # 2. Set job name (random string from Bubble)
    # job_name = str(uuid.uuid4())
    job_name = event['queryStringParameters']['job_name']
    
    # 3. Specify audio file location
    file_uri = event['queryStringParameters']['file_uri']
    job_uri = f'https:{file_uri}'
    
    # 3.b - Enable speaker labels (2nd pass)
    settings = {
	    'ShowSpeakerLabels': True,
	    'MaxSpeakerLabels': 2
	    }
	
    # 4. Call Transcribe, store in 'job' variable
    job = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        LanguageCode='en-US',
        Settings=settings
    )
    
    # 5. Extract job status; not strictly necessary, but useful to check that job started successfully
    job_status = job['TranscriptionJob']['TranscriptionJobStatus']
    
    # 6. Return job status
    return {
        'statusCode': 200,
        'body': json.dumps(job_status)
    }
