from django.shortcuts import render, redirect
from .forms import AudioFileForm
from .models import AudioFile
import librosa
import numpy as np
import pickle

# Load the models and scaler
models = pickle.load(open('C:/Users/anjal/OneDrive/Desktop/MiniProject/audiogenre/predictions/models.p', 'rb'))
scaler = models['scaler']
knn_best = models['knn']
svm_best = models['svm']
lookup_genre_name = models['lookup_genre_name']

def get_metadata(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=27)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    return mfccs_mean

def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            audio_features = get_metadata(audio_file.file.path)
            audio_features_scaled = scaler.transform([audio_features])

            genre_prediction_knn = knn_best.predict(audio_features_scaled)
            genre_prediction_svm = svm_best.predict(audio_features_scaled)

            context = {
                'form': form,
                'knn_prediction': lookup_genre_name[genre_prediction_knn[0]],
                'svm_prediction': lookup_genre_name[genre_prediction_svm[0]],
                'file_url': audio_file.file.url
            }
            return render(request, 'predictions/upload_file.html', context)
    else:
        form = AudioFileForm()
    return render(request, 'predictions/upload_file.html', {'form': form})
