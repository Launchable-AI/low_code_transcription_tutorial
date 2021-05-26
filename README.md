# Low Code Transcription

This is the source code from our low code transcription tutorial, which can be found here:
[link to tutorial on
YouTube](https://www.youtube.com/watch?v=_cEQoP6_u6k)

The 2 folders - GetTranscriptionJob and StartTranscriptionJob - each house the code for
a single AWS Lambda function.  The StartTranscriptionJob lambda function requires only
a lambda_function.py, whereas the GetTranscriptionJob lambda function requires both the
lambda_function.py and and an additional convo_parser.py, which does speaker label and
timestamp extraction.  You can move this code to you own lambda functions either by
copy-pasting the code, uploading the individual files into lambda functions, or creating
a deployment package (particularly for the GetTranscriptionJob files), which is
effectively just zipping and uploading to Lambda a directory with your source code files;
see here for details on AWS Lambda deployment packages: [link to lambda deployment package
documentation](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html).

Please note: as mentioned in the tutorial, this code is not production-ready.  It is
intended as a companion to the tutorial mentioned above, and as starting point, but should
not be relied upon without additional work.  The convo_parser code, in particular, has
some known bugs: e.g., if you enable speaker labels (i.e., speaker diarization) for an
audio file, but the AWS Transcribe API only detects a single speaker, the returned
transcript result will be just the final segment of the transcript.
