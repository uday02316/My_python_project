import cv2

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'q' to stop the camera.")

try:
    while True:
        # Capture each frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video.")
            break

        # Convert the frame to grayscale (needed for Haar cascade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the frame with detected faces
        cv2.imshow('Face Detection', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Stopping the camera...")
            break
finally:
    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed successfully.")
