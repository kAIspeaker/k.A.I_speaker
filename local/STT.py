import speech_recognition as sr
import make_audio

def speech_to_text():
	make_audio.mic()
	r = sr.Recognizer()

	harvard = sr.AudioFile('output.wav')
	with harvard as source:
		print('고객 응답: ', end='')
		audio = r.record(source)
	recognized_text = r.recognize_google(audio, language='ko-KR')

	# with sr.Microphone() as source:
		# print('고객 응답: ', end='')
		# r.adjust_for_ambient_noise(source, duration = 1)
		# audio = r.listen(source)
	# recognized_text = r.recognize_google(audio, language='ko-KR')

	try:
		print(recognized_text, '\n')
	except sr.UnknownValueError:
		print("Could not understand audio.")

	return recognized_text
