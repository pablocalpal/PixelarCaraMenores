from retinaface import RetinaFace
import cv2
import matplotlib.pyplot as plt

# Cargar la imagen
img_path = "img2.jpg"
img = cv2.imread(img_path)

# Detectar las caras
resp = RetinaFace.detect_faces(img_path)

# Dibujar los cuadrados alrededor de las caras detectadas
for key in resp:
    face = resp[key]
    facial_area = face["facial_area"]
    x1, y1, x2, y2 = facial_area
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Mostrar la imagen original con los cuadrados
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
# Extraer y mostrar las caras
faces = RetinaFace.extract_faces(img_path=img_path, align=True)
plt.show()

for face in faces:
    plt.imshow(face)
    plt.axis("off")
    plt.show()
