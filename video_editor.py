from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

class VideoEditor:
    def __init__(self, file, transcript):
        self.file = file
        self.transcript = transcript

    def edit_video(self):
        video_clip = VideoFileClip(self.file)

        for entry in self.transcript['transcripts']:
            start_time = entry['content'][0]['start']
            end_time = entry['content'][-1]['start'] + entry['content'][-1]['duration']

            output_filename = f"{entry['virality_score']}_{self.file}"
            video_segment = video_clip.subclip(start_time, end_time)

            # Create subtitle clips
            subtitles = [TextClip(text_entry['text'], fontsize=24, color='white').set_position(('center', 'bottom')).set_start(text_entry['start']) for text_entry in entry['content']]
            
            # Overlay subtitles on the video segment
            video_with_subtitles = CompositeVideoClip([video_segment] + subtitles)

            # Write the video file with subtitles
            video_with_subtitles.write_videofile(output_filename, codec='libx264', audio_codec='aac')

        video_clip.close()

if __name__ == '__main__':
    v = VideoEditor('-FSljXeiOAw.mp4', transcription_data)
    v.edit_video()
