import librosa
import librosa.display as ld
import numpy as np

def main():
	y, sr = librosa.load("./music.wav", mono=True)
	getNotes(y, sr)


def getNotes(y, sr):

	y_harmonic, y_percussive = librosa.effects.hpss(y)
	chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

	# Zeros out everything that is below 0.75 for clarity purposes
	for i in range(0, len(chroma)):
		for j in range(0, len(chroma[i])):
			if (chroma[i][j] < 0.80):
				chroma[i][j] = 0


	tuple_list = []
	note_row = 0 # 0,1,2,3,... ---> C,C#,D,D#,...

	for n in range(0, len(chroma)):

		num_zeros = 0
		note_length = 0
		start_index = 0
		current_index = 0
		i = 0

		while (i < len(chroma[note_row])):

			# Found a value that could lead to possible note
			if (chroma[note_row][i] > 0.0):
				num_zeros = 0
				note_length = 0

				# By incrementing the current_index and checking for zeros,
				# we allow only 3 zeros in the middle of notes and continue
				# to increment note_length until 3 zeros are found.
				while (num_zeros != 3):
					if (current_index > (len(chroma[note_row]) - 1)):
						break
					if (chroma[note_row][current_index] == 0.0):
						num_zeros += 1
					note_length += 1
					current_index += 1

				# satisfied note_length...add note to list
				if (note_length > 12):

					note_name = getName(note_row)
					beg_time = (float(start_index) / 43.0)
					length_time = (float(current_index) / 43.0) - beg_time
					tuple_list.append((note_name, beg_time, length_time))

	            # Loop stuff, to make sure we are
	            # scanning the correct portion of the chroma.
				start_index = current_index
				i = current_index
			else:
				i += 1
				start_index += 1
				current_index += 1

		note_row += 1

	tuple_list.sort(key=lambda x: x[1])

	# for i in tuple_list:
	# 	print(i)

	# Plotting chroma for correctness
	# plot_title_style = {"size": 8}
	# rc("font", **plot_title_style)
	# plt.style.use("dark_background")
	# plt.subplot(211)
	# plt.title("Chromagram")
	# librosa.display.specshow(chroma, x_axis="time", y_axis="chroma")
	# plt.colorbar()
	# plt.show()
	# plt.tight_layout()

def getName(x):
	return {
		0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
		6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B",
	}[x]


if __name__ == "__main__":
	main()