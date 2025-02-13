import argparse
import sys
import librosa
import numpy as np
import soundfile as sf
from PIL import Image
import cv2

def rangeToFreqIndices(min_freq, max_freq, bin_freqs):
    indices = [-1,-1]
    for i in range(len(bin_freqs)):
        if(bin_freqs[i]>min_freq and indices[0]==-1):
            indices[0] = i
        if(bin_freqs[i]>max_freq and indices[1]==-1):
            indices[1] = i-1
        if(indices[0]!=-1 and indices[1]!=-1):
            return indices

def s2a(input_filename, min_freq, max_freq, sample_rate, output_filename):
    img = Image.open(input_filename).convert("L")
    arry = np.flipud(np.asarray(img) / 255.0)
    empty_arry = np.zeros(arry.shape)
    
    bin_freqs = librosa.fft_frequencies(n_fft=(arry.shape[0]-1)*2, sr=sample_rate)
    freq_indices = rangeToFreqIndices(min_freq,max_freq,bin_freqs)
    
    bin_width = freq_indices[1]-freq_indices[0]
    resized_arry = cv2.resize(arry,(arry.shape[0], bin_width))
    
    empty_arry[freq_indices[0]:freq_indices[1],:] = resized_arry
    
    ranged_arry = empty_arry
    audio_signal = librosa.core.spectrum.griffinlim(ranged_arry)
    audio_signal /= np.max(np.abs(audio_signal),axis=0)
    sf.write(output_filename, audio_signal, sample_rate) 
 
def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Convert a spectrogram to audio with specified frequency range.")

    # Define the required arguments
    parser.add_argument('input_filename', type=str, help='Path to the input file (spectrogram image or data file)')
    parser.add_argument('min_freq', type=int, help='Minimum frequency in Hz for the output audio')
    parser.add_argument('max_freq', type=int, help='Maximum frequency in Hz for the output audio')
    parser.add_argument('sample_rate', type=int, help='Sample rate (Hz) for the audio output')
    parser.add_argument('output_filename', type=str, help='Name of the output audio file')

    # Parse the arguments
    args = parser.parse_args()

    # Call the s2a function with the provided arguments
    s2a(args.input_filename, args.min_freq, args.max_freq, args.sample_rate, args.output_filename)

if __name__ == "__main__":
    main() 

