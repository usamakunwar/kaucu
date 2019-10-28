
function authCallBack() {
    //console.log("Auth CallBack "+passengerId)
    setFiles()

}
function saveSignInClose() {
    new ButtonActive('save').start()
    if(firebase.auth().currentUser != null) {
        saveAndClose()
    } else {
        //console.log("No User")
        authCallBackTask = saveAndClose
        firebase.auth().signInAnonymously().catch(function(error) {
            if(error != null) { 
                new ButtonActive('save').stop()
                alert(error) 
            } 
        });
    }
}

function setData(passenger) {
    if(passenger.status != Status.Complete && passenger.status != Status.Incomplete) {
        readOnly = true
    } 
    setReadOnly()

    if(passenger.files != null) {
        files = passenger.files
    }

    setFiles()

    var preFill = null
    if(passenger.mahram != null) {
        preFill = passenger.mahram.firstName+" "+passenger.mahram.lastName
    }
    checkMahram(preFill)
}




function setFiles() {
    Object.values(DocumentType).forEach(function(docType) {

        var hidden = false
        if (docType == DocumentType.Permit) {
            hidden = !needsPermit()
            changeSizeFiles(hidden)
        }
        
        if (files.length == 0) {
            new FileActive(docType).set(null, hidden, readOnly)
            return
        } 
        var file = files.filter(function (file) { return file.documentType == docType })
        if(file.length > 0) {
            fileURL(passengerId, file[0], function(url) {
                if(docType == DocumentType.Visa) {
                    $('#status').html('<a class="text-white" target="_blank" href="'+url+'">Download Visa</a>') 
                } else {
                    new FileActive(docType).set(url, hidden, readOnly)
                }
            })
        } else {
            new FileActive(docType).set(null, hidden, readOnly)
        }
    });
}
function changeSizeFiles(hidden) {
    if(!hidden){
        //console.log('Add class')
        $('#files .col-md-6').addClass('col-md-4')
        $('#files .col-md-6').removeClass('col-md-6')
    } else {
        $('#files .col-md-4').addClass('col-md-6')
        $('#files .col-md-4').removeClass('col-md-4')
    }
}


function deleteFile(docType){
    //console.log("Deleting File "+docType)
    var index = files.map(function(e) { return e.documentType; }).indexOf(docType);
    var ref = storage.ref(firebase.auth().currentUser.uid)

    var deleteRef = fileStorageRef(passengerId, files[index])
    // Delete the file
    deleteRef.delete().then(function() {
        //console.log("Deleted!!")
        files = removeFromArray(index, files)
        save(function() {
            setFiles()
        })
    }).catch(function(error) {
        showAlert("Error", "Could not delete file "+JSON.stringify(error), true)

    });
}

function setReadOnly() {
    $('input, select').attr('readonly', readOnly);
    $('input, select').prop( "disabled", readOnly);
    $('#dialogDelete').prop( "disabled", readOnly);
    $('#save').prop('disabled', readOnly);
}

function fileUploadCallBack(file) {
    if(file.documentType == DocumentType.Passport) {
        scanPassport(file, function(passenger) {
            setReadOnly()
            new ButtonActive('save').enable()
            if(passenger != null) {
                //Comes back as a json string, so make date again
                if(passenger.dateOfBirth != null) {
                    passenger.dateOfBirth = new Date(passenger.dateOfBirth)
                }
                if(passenger.passportExpiry != null) {
                    var expiry = new Date(passenger.passportExpiry)
                    if(expiry < minPassportExpiry) {
                        showAlert('Passport expired', 'The minimum validity of a passport for visa has to be 6 months', true)
                    } else {
                        passenger.passportExpiry = expiry
                    }
                }
                //console.log(passenger.passportExpiry)
                passenger.status = Status.Incomplete
                files.push(file)
                setData(passenger)
                save()
            } else {
                files.push(file)
                loadFile(file)
                save()
                showAlert('Passport scan failed','Please enter details manually or retry with a different image', true)
            }
            checkValid()
        })
    } else {
        files.push(file)
        loadFile(file)
        save()
        checkValid()
    }
}
function loadFile(file) {
    fileURL(passengerId, file, function(url) {
        new FileActive(file.documentType).set(url, false, false)  
    })
}

function scanPassport(file, callBack) {
    //console.log("Scanning Passport")
    new FileActive(file.documentType).scanning(Activity.Scanning)
    var filePath = fileStoragePath(passengerId, file)
    $.ajax({
        url: '/vision',
        type: 'POST',
        data: {'filePath':filePath},
        success: function(passenger){
            callBack(passenger)
        },
        error: function(error){
            callBack(null)
        }
    });
}


function isValid() {
    if(get('firstName') == null) { return false }
    if(get('lastName') == null) { return false }
    if(getDateValue('dateOfBirth') == null) { return false }
    if(get('nationality') == null) { return false }
    if(get('gender') == null) { return false }
    if(get('passportNumber') == null) { return false }
    if(getDateValue('passportExpiry') == null) { return false }
    if(getDateValue('departureDate') == null) { return false }
    if(getDateValue('returnDate') == null) { return false }

    if(needsPermit()) {
        if(files.length < 3) {
            return false
        }
    } else {
        if(files.length < 2) {
            return false
        }
    }
    var needsMahram = isMahramNeeded()
    if(needsMahram.relation) {
        if(get('relationship') == null) {
            return false
        }
    }
    if(needsMahram.mahram) {
        if(getSelectedData('mahram') == null) {
            return false
        } 
    }
    return true
}

function checkValid() {
    var valid = isValid()
    //console.log("checkValid "+valid)
    var status = $('#status')
    status.empty()
    
    if(valid) {
        status.text(Status.Complete)
        status.css("background-color","#"+statusColor(Status.Complete))
    } else {
        status.text(Status.Incomplete)
        status.css("background-color","#"+statusColor(Status.Incomplete))
    }
}

function needsPermit() {
    var nationality = get('nationality')
    if(nationality == "United Kingdom" || nationality == null) {
        return false
    } else {
        return true
    }
}
function isMahramNeeded() {
    var needsRelation = needsRelationship()
    var needsMahram = false
    if (needsRelation) {
        if(get('relationship') != 'Women Group') {
            needsMahram = true
        }
    } else {
       needsMahram = false
    }
    return {'relation':needsRelation, 'mahram':needsMahram}
}
function needsRelationship() {
    var dateOfBirth = getDateValue('dateOfBirth')
    if(dateOfBirth != null) {
        if (getAge(dateOfBirth) <= 17) {
            return true
        }
    } 
    if(get('gender') == Gender.Female) {
        return true
    }
    return false
}

function checkMahram(preFill) {
    var needsMahram = isMahramNeeded()
    var nrelation = $('#nrelation')
    var nmahram = $('#nmahram')
    if(needsMahram.relation) {
        nrelation.removeClass('hide')
    } else {
        nrelation.addClass('hide')
    } 
    if(needsMahram.mahram) {
        if(mahrams == null) {
            getMahrams(mahramCallback, preFill)
        }
        nmahram.removeClass('hide')
    } else {
        nmahram.addClass('hide')
    }
}

function getMahrams(callBack, preFill) {
    //console.log("getMahrams "+mahrams)
    var ref = db.collection("Client").doc(firebase.auth().currentUser.uid).collection("Passenger")
    ref.where("gender", "==", Gender.Male).get().then(function(querySnapshot) {
        var mahrams = []
        querySnapshot.forEach(function(doc) {
            const data = doc.data()
            var dob = data['dateOfBirth']
            if(dob != null) {
                //console.log(formarDate(dob.toDate()))
                var age = getAge(dob.toDate())
                if(age > 17) {
                    var mahram = {}
                    mahram['firstName'] = data.firstName
                    mahram['lastName'] = data.lastName
                    mahram['passportNumber'] = data.passportNumber
                    mahram['id'] = doc.id
                    mahrams.push(mahram)
                }
             }
        });
        callBack(mahrams, preFill)
    })
    .catch(function(error) {
        //console.log("Error getting mahrams: ", error);
    });
}

function mahramCallback(_mahrams, preFill) {
    mahrams = _mahrams
    //console.log("Got mahrams "+mahrams.length+ " Prefill "+preFill)
    $('#mahram').empty()
    $('#mahram').append('<option disabled selected value>Select</option>')
    mahrams.forEach(function(mahram, key){
        var mahramString = JSON.stringify(mahram)
        $('#mahram').append('<option data-value='+mahramString+'>'+mahram.firstName+' '+mahram.lastName+'</option>')
    })
    if(preFill != null) {
        $('#mahram').val(preFill)
    }
}

$('input,select').change(function() {
    checkValid()
});
//changeDate does not fire if user types complete date (instead of selecting)
$( "#gender,#nationality,#relationship,#dateOfBirth" ).change(function() {
    checkMahram(null)
});
$( "#dateOfBirth" ).on('changeDate', function(e) {
    checkMahram(null)
});



//If text was entered that was not a nationality, double check it
$('#nationality').change(function() {
    var exists = countries.includes(this.value)
    if(!exists) {
        this.value = null
    }
});



var minDOB = new Date()
$('#dateOfBirth').datepicker({
    format: 'dd/mm/yyyy',
    keyboardNavigation: false,
    forceParse: true,
    autoclose: true,
    endDate: minDOB,
    startView: 'years',
}).on('changeDate', function(e) {
    checkValid()
});
$('#dateOfBirth').datepicker('setEndDate', minDOB);

var minPassportExpiry = minPassportExpiryDate()
$('#passportExpiry').datepicker({
    format: 'dd/mm/yyyy',
    keyboardNavigation: false,
    forceParse: true,
    autoclose: true,
    startView: 'years',
    startDate: minPassportExpiry,
}).on('changeDate', function(e) {
    checkValid()
});

$('#departureDate, #returnDate').datepicker({
    format: 'dd/mm/yyyy',
    keyboardNavigation: false,
    forceParse: true,
    autoclose: true,
    startDate: config.minDepartureDate,
}).on('changeDate', function(e) {
    checkValid()
});

$('#nationality').typeahead({ source: countries, 
    afterSelect: function(item) {
        //console.log("SELECTED")
        setFiles()
    }
});



$('#relationship').append('<option disabled selected value>Select</option>')
Object.values(Relationship).forEach(function(relation) {
    $('#relationship').append('<option value="'+relation+'">'+relation+'</option>')
});

$('#gender').append('<option disabled selected value>Select</option>')
Object.values(Gender).forEach(function(gender) {
    $('#gender').append('<option value="'+gender+'">'+gender+'</option>')
});


