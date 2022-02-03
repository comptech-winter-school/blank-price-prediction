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
          var fileName = this.files[0].name
          var fileType = this.files[0].type

          if (file.length == 1 && validateFileType(fileType)) {
                console.log(fileType)
                document.getElementById("upload-text").innerHTML =  "Файл: " + fileName
                enablePredictButton()
              }
          else {
              alert ("Ivalid file extension")
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