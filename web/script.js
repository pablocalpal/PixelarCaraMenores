document.addEventListener("DOMContentLoaded", () => {
  // Elementos del DOM
  const imageInput = document.getElementById("image-input")
  const uploadButton = document.getElementById("upload-button")
  const originalImageContainer = document.getElementById("original-image-container")
  const modifiedImageContainer = document.getElementById("modified-image-container")
  const loadingElement = document.getElementById("loading")
  const errorMessageElement = document.getElementById("error-message")

  // Variables para almacenar datos
  let selectedFile = null

  // Event listeners
  imageInput.addEventListener("change", handleImageSelection)
  uploadButton.addEventListener("click", uploadImage)

  // Función para manejar la selección de imagen
  function handleImageSelection(event) {
    const file = event.target.files[0]

    if (file && file.type.startsWith("image/")) {
      selectedFile = file
      displayOriginalImage(file)
      uploadButton.disabled = false

      // Limpiar el contenedor de imagen modificada y mensajes de error
      modifiedImageContainer.innerHTML = `
        <div class="placeholder">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <p>La imagen transformada aparecerá aquí</p>
        </div>
      `
      hideError()
    } else {
      selectedFile = null
      uploadButton.disabled = true
      showError("Por favor, selecciona un archivo de imagen válido.")
    }
  }

  // Función para mostrar la imagen original
  function displayOriginalImage(file) {
    const reader = new FileReader()

    reader.onload = (e) => {
      originalImageContainer.innerHTML = ""
      const img = document.createElement("img")
      img.src = e.target.result
      img.alt = "Imagen original"
      originalImageContainer.appendChild(img)
    }

    reader.readAsDataURL(file)
  }

  // Función para subir la imagen a la API
  function uploadImage() {
    if (!selectedFile) {
      showError("Por favor, selecciona una imagen primero.")
      return
    }

    // Mostrar indicador de carga
    showLoading()

    // Crear FormData para enviar el archivo
    const formData = new FormData()
    formData.append("image", selectedFile)

    // Configuración de la petición
    // Nota: Reemplaza la URL con la de tu API real
    const apiUrl = "https://tu-api.com/procesar-imagen"

    fetch(apiUrl, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error en la respuesta: ${response.status} ${response.statusText}`)
        }
        return response.blob()
      })
      .then((imageBlob) => {
        displayModifiedImage(imageBlob)
        hideLoading()
      })
      .catch((error) => {
        console.error("Error:", error)
        hideLoading()
        showError("Error al procesar la imagen. Por favor, intenta de nuevo más tarde.")

        // Para fines de demostración, simulamos una respuesta exitosa
        // En un entorno real, elimina este código
        setTimeout(() => {
          simulateSuccessResponse()
        }, 1000)
      })
  }

  // Función para mostrar la imagen modificada
  function displayModifiedImage(imageBlob) {
    const imageUrl = URL.createObjectURL(imageBlob)

    modifiedImageContainer.innerHTML = ""
    const img = document.createElement("img")
    img.src = imageUrl
    img.alt = "Imagen modificada"
    modifiedImageContainer.appendChild(img)
  }

  // Funciones auxiliares para UI
  function showLoading() {
    loadingElement.classList.remove("hidden")
  }

  function hideLoading() {
    loadingElement.classList.add("hidden")
  }

  function showError(message) {
    errorMessageElement.textContent = message
    errorMessageElement.classList.remove("hidden")
  }

  function hideError() {
    errorMessageElement.classList.add("hidden")
  }

  // Función para simular una respuesta exitosa (solo para demostración)
  // En un entorno real, elimina esta función
  function simulateSuccessResponse() {
    if (selectedFile) {
      const reader = new FileReader()

      reader.onload = (e) => {
        modifiedImageContainer.innerHTML = ""
        const img = document.createElement("img")
        img.src = e.target.result
        img.style.filter = "sepia(70%) hue-rotate(180deg)" // Filtro más moderno
        img.alt = "Imagen modificada"
        modifiedImageContainer.appendChild(img)
        hideLoading()
      }

      reader.readAsDataURL(selectedFile)
    }
  }
})
