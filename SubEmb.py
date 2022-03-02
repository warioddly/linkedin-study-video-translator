import imp
from subprocess import call

def EmbeddingSubtitle(language, nameVideo, subtitle, nameOutputVideo):
    args = "inlcudes/ffmpeg.exe -i" +  ' "Files/' + nameVideo + '.mp4"'  + ' -vf ' + '"subtitles=' + 'Files/' + subtitle + '_' + language + '.srt:force_style=' + "'OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=17'" + '"' + ' "Files/' + nameOutputVideo + "_" + language + '_sub.mp4"'
    call(args, shell=False)


language = input("Введите язык (kg or ru): ")
video = input("Введите название видео: ")
EmbeddingSubtitle(language, video, video, video)

input("\nНажмите ENTER чтобы выйти")