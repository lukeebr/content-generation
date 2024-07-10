from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
from urllib.parse import parse_qs
from openai import OpenAI
import json

class ContentParser:
    def __init__(self):
        self.client = OpenAI(api_key='')

    def get_video_id(self, url):
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)['v'][0]

    def retrieve_transcript(self, url):
        video_id = self.get_video_id(url)
        return YouTubeTranscriptApi.get_transcript(video_id)
    
    def parse_transcript(self, transcript, topic, target_audience):
        SYSTEM_PROMPT = '''
        You are an assistant tasked to extract elements from a list in a transcript.
        Your goal is to create attention grabbing short form videos from a transcript.
        The script should have a total duration of around 30 seconds.
        You will not edit nor merge the transcript elements and will return them in the same format as they were input and in the correct order that they were input, not removing any text between.
        It is very important that the transcript text is not edited for the transcript text to be the correct size for viewing on screen.
        You will also include a reasoning of why the segment is engaging for viewers and give it a virality score from 0/100.

        You will extract based on a topic and target audience for the returned transcript.

        TOPIC : ''' + topic + ''' 

        TARGET AUDIENCE: ''' + target_audience + ''' 

        Your response will be in JSON.
        
        Sample response:

        {
            "transcripts": [
                {
                    "virality_score": 78,
                    "reason": "",
                    "content": [
                    {
                        "text":"the jogan experience I feel like there's",
                        "start":0.32,
                        "duration":4.959
                    },
                    {
                        "text":"like a backlash happening you know I",
                        "start":2.8,
                        "duration":4.36
                    },
                    {
                        "text":"feel like it's interesting like being",
                        "start":5.279,
                        "duration":3.601
                    },
                    {
                        "text":"pregnant you really I've started getting",
                        "start":7.16,
                        "duration":3.08
                    },
                    {
                        "text":"like obsessed with you know everything",
                        "start":8.88,
                        "duration":3.04
                    },
                    {
                        "text":"you put in your body you know and just",
                        "start":10.24,
                        "duration":3.439
                    },
                    {
                        "text":"the idea of just drinking water is like",
                        "start":11.92,
                        "duration":3.28
                    },
                    {
                        "text":"a full-time job like where am I getting",
                        "start":13.679,
                        "duration":3.161
                    },
                    {
                        "text":"my water right I got it because it's",
                        "start":15.2,
                        "duration":3.079
                    },
                    {
                        "text":"either my choices are",
                        "start":16.84,
                        "duration":5.199
                    },
                    {
                        "text":"fluoride or microplastics and I'm not",
                        "start":18.279,
                        "duration":5.281
                    }
                    ]
                },
                {
                    "virality_score": 84,
                    "reason": "This segment covers a wide range of topics from health choices to consumer products, including shocking facts about chemicals in everyday items. It also delves into the controversy surrounding Bill Gates and his views on environmental issues. The variety of engaging and controversial topics discussed in this segment makes it highly shareable and likely to spark a discussion among viewers.",
                    "content": [
                            {
                                "text":"unreal that's crazy this is Reuters I",
                                "start":166.64,
                                "duration":5.64
                            },
                            {
                                "text":"want to say it was in St Louis but they",
                                "start":170.56,
                                "duration":4.959
                            },
                            {
                                "text":"it was over 50,000 lawsuits oh my God",
                                "start":172.28,
                                "duration":5.76
                            },
                            {
                                "text":"that's so crazy Johnson Johnson didn't",
                                "start":175.519,
                                "duration":3.961
                            },
                            {
                                "text":"tell the FDA that at least three tests",
                                "start":178.04,
                                "duration":3.8
                            },
                            {
                                "text":"by three three different Labs from 72 to",
                                "start":179.48,
                                "duration":5.44
                            },
                            {
                                "text":"75 it found aestus in his talc in one",
                                "start":181.84,
                                "duration":5.8
                            },
                            {
                                "text":"case that levels reported as rather High",
                                "start":184.92,
                                "duration":3.84
                            }
                            ]
                }
            ]
        }
        '''

        USER_PROMPT = f'''
        {transcript}
        '''

        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT}
            ]
        )

        return json.loads(response.choices[0].message.content)
