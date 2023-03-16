# -*- coding: utf-8 -*-
"""
Created on 12.11.2022 

@author: Mustafa Melih TÜFEKCİOĞLU -B191210004
         Deniz Berfin TAŞTAN       -B181210010 
"""

import cv2 #görüntü işleme için kullanılır.
import mediapipe as mp #el yüz tanıma gibi nesne algılama işlemleri yapan makine öğrenmesi çözümleri içerir.
from firebase import firebase

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


firebase = firebase.FirebaseApplication("https://database-b0c01-default-rtdb.firebaseio.com/", None)

# Kamera islemleri
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
       
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) #Kamera açısı ve renk ayarlama
        image.flags.writeable = False #performans arttırmak için görüntü yazılamaz hale getirilir. Sadece okunur.
        results = hands.process(image) #görüntü alınır.

        image.flags.writeable = True #El noktaları çizilmesi için yazma işlemine izin verilir.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                ## el açık ve kapalı iken ekrana yazdırma
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y  # 9.nokta x,y
                x1, y1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y #12.nokta x,y

                font = cv2.FONT_HERSHEY_PLAIN

                if y1 > y: # el kapalı
                    cv2.putText(image, "KAPALI", (10, 50), font, 3, (0, 0, 0), 3)
                    firebase.put('/' , 'data', "0") # firebase led durumunu 0 yapar
                else:
                    cv2.putText(image, "ACIK", (10, 50), font, 3, (0, 0, 0), 3)
                    firebase.put('/' , 'data', "1") # firebase led durumunu 1 yapar

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        cv2.imshow('IOT PROJECT', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
       