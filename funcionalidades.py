# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:11:45 2024

@author: DAM
"""

import os
import pygame
import yt_dlp  

# Inicializa el mezclador de Pygame
pygame.mixer.init()

# Lista para almacenar las canciones en cola
song_queue = []
current_song_title = None  # Rastrea el título de la canción actual

# Asegúrate de que el directorio de música exista
music_directory = "music"
if not os.path.exists(music_directory):
    os.makedirs(music_directory)

def play_song(video_id, title):
    """Reproduce la canción usando su ID de video."""
    global current_song_title
    url = f'https://www.youtube.com/watch?v={video_id}'
    print(f"Reproduciendo canción desde: {url}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': '',#Añade tu localización de FFMPEG
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(music_directory, f'{title}.%(ext)s'),  # Guarda con el título de la canción en el directorio /music
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Carga y reproduce la canción descargada
        pygame.mixer.music.load(os.path.join(music_directory, f'{title}.mp3'))
        pygame.mixer.music.play()
        current_song_title = title  # Establece el título de la canción actual
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def queue_song(video_id, title):
    """Agrega una canción a la cola y la reproduce inmediatamente."""
    song_queue.append((video_id, title))
    print(f"{title} ha sido agregada a la cola.")
    if len(song_queue) == 1:  # Si es la primera canción en la cola, reproduce
        play_song(video_id, title)

def skip_song():
    """Salta la canción que se está reproduciendo actualmente."""
    pygame.mixer.music.stop()
    if song_queue:
        next_song = song_queue.pop(0)
        play_song(next_song[0], next_song[1])
    else:
        print("No hay más canciones en la cola.")

def stop_music():
    """Detiene la música que se está reproduciendo actualmente."""
    pygame.mixer.music.stop()
    print("Música detenida.")

def search_saved_music():
    """Lista los archivos de música guardados."""
    saved_music = os.listdir(music_directory)
    if saved_music:
        print("Archivos de música guardados:")
        for song in saved_music:
            print(song)
    else:
        print("No se encontró música guardada.")

def cleanup_current_song():
    """Elimina el archivo de la canción actual si existe."""
    if current_song_title:
        try:
            os.remove(os.path.join(music_directory, f'{current_song_title}.mp3'))
            print(f"Eliminado {current_song_title}.mp3")
        except Exception as e:
            print(f"No se pudo eliminar {current_song_title}.mp3: {e}")
