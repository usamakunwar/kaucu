var storage = firebase.storage();
storage.setMaxUploadRetryTime(1000)

function fileUploader(fileInput) {
    console.log(fileInput)
    if(fileInput.files.length == 0) {
        return
    }
    new FileActive(fileInput.name).start()
    if (passengerId == "") {
        save()
    }
    checkFileSize(fileInput.files[0].size, function(isValid) {
        if(isValid) {
            getFileDimensions(fileInput.files[0], function(width, height) {
                var file = {}
                file.documentType = fileInput.name
                file.extn = fileInput.files[0].name.split('.').pop();
                file.fileType = 'image'
                file.width = width
                file.height = height
                console.log(file)
                getFileID(function(fileId) {
                    file.id = fileId
                    uploadFile(fileInput, file, fileUploadCallBack)
                })
            })
        } else {
            new FileActive(fileInput.name).stop()
            showAlert('File size too big', "Maximum file size allowed is 4MB", true)
        }
    })
}

function uploadFile(fileInput, file, callBack) {
    console.log("Uploading File "+passengerId)
    var fileObject = fileInput.files[0]
    var uploadRef = fileStorageRef(passengerId, file)
    var uploadTask = uploadRef.put(fileObject)
    // Listen for state changes, errors, and completion of the upload.
    new FileActive(fileInput.name).upload()
    uploadTask.on(firebase.storage.TaskEvent.STATE_CHANGED, // or 'state_changed'
        function(snapshot) {
            // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
            var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            //console.log('Upload is ' + progress + '% done');
            new FileActive(fileInput.name).progress(Math.round(progress))            
        }, 
        function(error) {
        // A full list of error codes is available at
        // https://firebase.google.com/docs/storage/web/handle-errors
            console.log("Error "+error.code)
            new FileActive(fileInput.name).stop()
            showAlert('Error', 'Check your internet connection '+error.code, true)
        }, 
        function() {
        // Upload completed successfully
            console.log('Uploaded a blob or file!');
            if(file.extn == 'pdf') {
                new FileActive(fileInput.name).converting()
                pdf2Image(passengerId, file.documentType, function(error, result) {
                    if(error) {
                        console.log("Error "+error)
                        new FileActive(fileInput.name).stop()
                        showAlert('Error', 'Could not convert PDF '+error, true)
                    } else {
                        console.log("RESULT "+result.width+" "+result.height+" "+result.extn)
                        file.extn = result.extn
                        file.width = result.width
                        file.height = result.height
                        callBack(file)
                    }
                })
            } else {
                callBack(file)
            }
        }
    );
}

function pdf2Image(passengerId, documentType, callBack) {
    console.log("PDF 2 Image Starts")
    var data = {}
    data.clientId = firebase.auth().currentUser.uid
    data.passengerId = passengerId
    data.documentType = documentType
    $.ajax({
        url: '/pdf2image',
        type: 'POST',
        data: data,
        success: function(response){
            callBack(null, response)
        },
        error: function(error){
            callBack(error, null)
        }
      });
}

function fileURL(passengerId, file, callBack) {
    var ref = fileStorageRef(passengerId, file)
    ref.getDownloadURL().then(function(downloadURL) {
        if(downloadURL == null) {
            console.log("ERROR "+downloadURL)
        }
        console.log(downloadURL)
        callBack(downloadURL)
    });
}

function fileStorageRef(passengerId, file) {
    return storage.ref(firebase.auth().currentUser.uid).child(passengerId)
    .child(passengerId+"_"+file.documentType+"."+file.extn)
}
function fileStoragePath(passengerId, file) {
    return firebase.auth().currentUser.uid+'/'+passengerId+"/"+passengerId+"_"+file.documentType+"."+file.extn
}
