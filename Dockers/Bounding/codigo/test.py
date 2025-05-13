from retinaface import RetinaFace
resp = RetinaFace.detect_faces("img1.jpg")

print(resp)

import matplotlib.pyplot as plt
faces = RetinaFace.extract_faces(img_path = "img1.jpg", align = True)
for face in faces:
  plt.imshow(face)
  plt.show()