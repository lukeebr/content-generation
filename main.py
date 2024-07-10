from content_parser import ContentParser
from video_editor import VideoEditor
from pytube import YouTube

class ContentGenerator:
    def __init__(self, URL, topic, target_audience):
        self.URL = URL
        self.content_parser = ContentParser()

        self.topic = topic
        self.target_audience = target_audience

        self.output_folder = '/output'

        self.file_extension = '.mp4'
        self.video_id = self.content_parser.get_video_id(URL)
        self.file_name = self.video_id + self.file_extension

        #self.download_video()
        self.generate_content()

    def download_video(self):
         yt = YouTube(self.URL)
         yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=self.file_name)

    def generate_content(self):
        self.transcript = self.content_parser.retrieve_transcript(self.URL)
        self.parsed_transcript = self.content_parser.parse_transcript(self.transcript, self.topic, self.target_audience)

        print(self.parsed_transcript)

        #self.video_editor = VideoEditor(self.file_name, self.parsed_transcript)
        #self.video_editor.edit_video()

if __name__ == '__main__':
    ContentGenerator('https://www.youtube.com/watch?v=-FSljXeiOAw&ab_channel=Valuetainment', 'Any', 'Youtube Shorts')