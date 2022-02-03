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
      if (file.length == 1) {
          enablePredictButton()
          }
      else {
          disablePredictButton()
      }
  }
  })
  }

function main() {
    uploadedFile()
}

main()