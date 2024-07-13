import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse

# Emotion dictionary
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
music_dist = {0: "songs/angry.csv", 1: "songs/disgusted.csv", 2: "songs/fearful.csv", 3: "songs/happy.csv", 4: "songs/neutral.csv", 5: "songs/sad.csv", 6: "songs/surprised.csv"}

def music_rec(emotion_index):
    df = pd.read_csv(music_dist[emotion_index])
    df = df[['Name', 'Album', 'Artist']]
    return df.head(15)

def index(request):
    return render(request, 'index.html', {'emotions': emotion_dict})

def recommendations(request, emotion_index):
    df1 = music_rec(emotion_index)
    headings = ["Name", "Album", "Artist"]
    data = df1.to_dict(orient='records')
    return render(request, 'recommendations.html', {'headings': headings, 'data': data})

def select_mood(request):
    if request.method == 'POST':
        selected_mood = int(request.POST['mood'])
        return redirect(reverse('recommendations', args=[selected_mood]))
