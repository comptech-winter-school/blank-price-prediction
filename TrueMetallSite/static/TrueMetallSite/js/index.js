// disable predict-button
function disablePredictButton() {
    document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById("predict-button").disabled = true;

    var predict_button = document.getElementById("predict-button");
    predict_button.style.opacity = 0.25;
  })
}

// enable predict-button
function enablePredictButton() {
    document.getElementById("predict-button").disabled = false;
    var predict_button = document.getElementById("predict-button");
    predict_button.style.opacity = 1;
  }

// check uploaded file
function uploadedFile() {
    disablePredictButton()

    document.addEventListener("DOMContentLoaded", function(event) {

    var uploadButton = document.getElementById("upload-button");
    uploadButton.addEventListener("change", handleFile, true);

      // handle uploaded file
    function handleFile() {
          var file = this.files;
          var fileLength = file.length
          var fileName = file[0].name
          var fileType = file[0].type

          // validation of files count and type
          if (fileLength == 1 && validateFileType(fileType)) {
                document.getElementById("upload-text").innerHTML =  "Файл: " + fileName
                enablePredictButton()
              }
          else {
              alert ("Недопустимое расширение файла")
          }
        }
    })
}

// validate type of upload file
function validateFileType(fileType) {
     return (
     fileType == "application/vnd.ms-excel"
     || fileType == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
     )
}

function main() {
    uploadedFile()
}

main()