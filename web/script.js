document.addEventListener("DOMContentLoaded", () => {
  // Elementos del DOM
  const imageInput = document.getElementById("image-input")
  const uploadButton = document.getElementById("upload-button")
  const originalImageContainer = document.getElementById("original-image-container")
  const modifiedImageContainer = document.getElementById("modified-image-container")
  const loadingElement = document.getElementById("loading")
  const errorMessageElement = document.getElementById("error-message")
  const debugCheckbox = document.getElementById("debug-checkbox")

  // Variables para almacenar datos
  let selectedFile = null

  // Event listeners
  imageInput.addEventListener("change", handleImageSelection)
  uploadButton.addEventListener("click", uploadImage)

  function handleImageSelection(event) {
    const file = event.target.files[0]

    if (file && file.type.startsWith("image/")) {
      selectedFile = file
      displayOriginalImage(file)
      uploadButton.disabled = false

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

  function uploadImage() {
    if (!selectedFile) {
      showError("Por favor, selecciona una imagen primero.")
      return
    }

    showLoading()

    const formData = new FormData()
    formData.append("file", selectedFile)

    // Agregar debug=true si el checkbox está marcado
    if (debugCheckbox.checked) {
      formData.append("debug", "true")
    }

    const apiUrl = "http://localhost:8000/pixelar_menores"

    fetchWithTimeout(apiUrl, {
      method: "POST",
      body: formData,
      timeout: 30000
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
      })
  }

  function displayModifiedImage(imageBlob) {
    const imageUrl = URL.createObjectURL(imageBlob)
    modifiedImageContainer.innerHTML = ""
    const img = document.createElement("img")
    img.src = imageUrl
    img.alt = "Imagen modificada"
    modifiedImageContainer.appendChild(img)
  }

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

  function fetchWithTimeout(resource, options = {}) {
    const { timeout = 30000 } = options

    return Promise.race([
      fetch(resource, options),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Tiempo de espera agotado")), timeout)
      )
    ])
  }
})
