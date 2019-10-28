
const DocumentType = {
    Passport: 'Passport',
    Photo: 'Photo',
    Permit: 'Permit',
    Visa : 'Visa'
}


const Activity = {
    Loading : 'Loading',
    Scanning: 'Scanning',
    Uploading: 'Uploading',
    Converting: 'Converting'
}

const Relationship = {
    Husband : "Husband",
    Son : "Son",
    Father : "Father",
    Brother : "Brother",
    GrandFather : "GrandFather",
    Nephew : "Nephew",
    Uncle : "Uncle",
    WomenGroup : "Women Group"
}

const Status =  {
    Cancelled : "Cancelled",
    Incomplete : "Incomplete",
    Complete : "Complete",
    Paid : "Paid",
    MofaComplete : "Got Mofa",
    PassportReceived : "Passport Received",
    VisaComplete : "Visa Complete",
    Dispatched : "Dispatched",
    Refunded : "Refunded"
}

const Gender = {
    Male: "Male",
    Female: "Female"
}


const PaymentStatus = {
    Pending : "Pending",
    Success : "Success",
    Error : "Error",
    ClientCancelled : "Client Cancelled",
}


function get(id) {
    var element = $('#'+id)
    return checkNull(element.val())
}

function getDateValue(id) {
    var date = $('#'+id).datepicker('getDate')   
    if (isValidDate(date)) {
        return date
    } else {
        return null
    }
}
function getSelectedData(id) {
    console.log(id)
    var element = $('#'+id).find(":selected").data("value")
    console.log("getSelectedData "+element)
    //console.log("Have "+checkNull(element))
    return checkNull(element)
}

function checkNull(value) {
    if(value == null) {
        return null
    } else if(value == "") {
        return null
    }
    return value
}
function isValidDate(d) {
    return d instanceof Date && !isNaN(d);
}

function minPassportExpiryDate() {
    var now = new Date();
    now.setMonth(now.getMonth()+6);
    return now
}
// function minDepartureDate(dateString) {
//     //Add a certain number of days to the departure start date (of season)
//     var date = new Date(dateString);
//     date.setDate(date.getDate()+3);
//     return date
// }

function formatDate(date) {
    var day = ("0" + date.getDate()).slice(-2);
    var month = ("0" + (date.getMonth() + 1)).slice(-2);
    var year = date.getFullYear();
  
    return day + '/' + month + '/' + year;
}
  
function getAge(birthday) { // birthday is a date
    var ageDifMs = Date.now() - birthday.getTime();
    var ageDate = new Date(ageDifMs); // miliseconds from epoch
    return Math.abs(ageDate.getUTCFullYear() - 1970);
}

function getFileID(callBack) {
    $.ajax({
        url: '/file',
        type: 'POST',
        success: function(data){
            callBack(data)
        },
        error: function(error){
            callBack(null)
        }
      });
}
function checkFileSize(size, callBack) {
    $.ajax({
        url: '/filesize',
        type: 'POST',
        data: {'fileSize':size},
        success: function(data){
            callBack(data)
        },
        error: function(error){
            callBack(null)
        }
      });
}
function getFileDimensions(file, callBack) {
    if(file.type == 'application/pdf') {
        callBack(null,null)
        return;
    }
    var fr = new FileReader;
    fr.onload = function() { // file is loaded
        var img = new Image;
        img.onload = function() {
            // image is loaded; sizes are available
            callBack(img.width,img.height)
        };
        img.src = fr.result; // is the data URL because called with readAsDataURL
    };
    fr.readAsDataURL(file) //
}

function statusColor(status) {
    switch(status) {
    case 'Cancelled':
        return 'f44242';
    case 'Incomplete':
        return 'e2ad00';
    case 'Complete':
        return 'f49741';
    case 'Paid':
        return '82f441';
    case 'Got Mofa':
        return 'ff00bb';
    case 'Passport Received':
        return 'd000ff';
    case 'Visa Complete':
        return '00ddff';
    case 'Dispatched':
        return '00a1ff';
    default:
        return 'f44242';
    }
}


class FileActive {
    constructor(objectId) {
      this.objectId = objectId
      this.object = $('#'+objectId)
    }

    set(url, hidden, readOnly) {
        if(hidden) {
            this.object.addClass('hide')
            return
        } else {
            this.object.removeClass('hide')
        }
        this.object.empty()
        this.object.unbind( "click" );

        if(url == null) {
            if(!readOnly) {
                this.setTitleClick()
                this.appendTitle()
            }
            this.object.css("background-image", "none")
        } else {
            this.setImageClick(url, readOnly)
            this.object.css("background-image", "url('"+url+"')")
            this.object.css("background-repeat", "no-repeat")
            this.object.css("background-position", "center")
            this.object.css("background-size", "cover")    
        }
    }

    upload() {
        this.object.empty()
        this.object.off('click')
        this.appendSpinner(Activity.Uploading)
    }

    
    start() {
        this.object.empty()
        this.object.off('click')
        this.appendSpinner(Activity.Loading)
    }
    
    progress(percent) {
       $('#'+this.objectId+'Progress').text(''+percent+' %')
    }
    
    scanning(activity) {
        this.object.empty()
        this.appendSpinner(Activity.Scanning)
    }
    converting(activity) {
        this.object.empty()
        this.appendSpinner(Activity.Converting)
    }

    stop() {
        this.object.empty()
        this.setTitleClick()
        this.appendTitle()
    }

    setTitleClick() {
        var sender = this
        var clickInput = function() {
            $('#'+sender.objectId+'Input').click()
        }
        this.object.click(function(event) {
            if(firebase.auth().currentUser != null) {
                clickInput()
            } else {
                console.log("No User")
                sender.start()
                authCallBackTask = clickInput
                firebase.auth().signInAnonymously().catch(function(error) {
                    if(error != null) { 
                        sender.stop()
                        showAlert('Error', error, true)
                    }
                });
            }
        })
    }




    setImageClick(url, readOnly) {
        var objectId = this.objectId
        this.object.click(function() {
            console.log(" Object Id "+objectId)
            if(objectId != DocumentType.Passport) {
                $('#dialogDelete').prop('disabled', readOnly)
                if(!readOnly) {
                    $('#dialogDelete').click(function() {
                        $("#dialogDismiss").click();
                        deleteFile(objectId)
                    });
                }
            } else {
                $('#dialogDelete').prop('disabled', true)
            }

            $('#dialogLabel').text(this.objectId)
            $('#dialogImage').attr('src',url);
            $("#"+objectId+"Button").click();
        });
    }



    appendTitle() {
        this.object.append('<div class="col-sm-12">+ Add '+this.objectId+'</div>')
    }

    appendSpinner(activity) {
        this.object.append(` 
                <div class="col-sm-12">
                    <div class="spinner-border align-middle" role="status"></div> 
                    <span class="ml-3 align-middle">
                        `+activity+`
                        <span id="`+this.objectId+`Progress"></span
                    </div>
                </div>
            `)
    }
  }


  class ButtonActive {
    constructor(objectId) {
      this.objectId = objectId
      this.object = $('#'+objectId)
    }
    start() {
        this.object.empty()
        this.disable()
        this.appendSpinner(Activity.Loading)
    }

    stop() {
        this.object.empty()
        this.enable()
        this.appendTitle()
    }

    enable() {
        this.object.prop('disabled', false)
    }
    disable() {
        this.object.prop('disabled', true)
    }


    appendTitle() {
        this.object.append(capitalizeFirstLetter(this.objectId))
    }

    appendSpinner(activity) {
        this.object.append(`
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        `+activity)
    }
  }

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function showAlert(title, message, error, dismiss) {
    $('#alertHeading').empty()
    $('#alertHeading').text(title)
    $('#alertMessage').empty()
    $('#alertMessage').text(message)
    
    if(error) {
        $('#alertContent').removeClass('alert-success')
        $('#alertContent').addClass('alert-danger')
    } else {
        $('#alertContent').removeClass('alert-danger')
        $('#alertContent').addClass('alert-success')
    }
    $('#AlertButton').click()
    if(dismiss) {
        $('#alertDismiss').click(function() {
            dismiss()
        });
    }
}
function showDone(message, dismiss) {
    $('#doneLabel').empty()
    $('#doneLabel').text(message)
    $('#DoneButton').click()
    $('#doneDismiss').click(function() {
        dismiss()
    });
}

function removeFromArray(index, array) {
    if (index > -1) {
        array.splice(index, 1);
    }
    return array
}

function makeSmallAndDash(title) {
    return title.replace(/\s+/g, '-').toLowerCase();
}


function dictIsEmpty(obj) {
    return Object.keys(obj).length === 0;
  }

function addHide(id) {
    $('#'+id).addClass('hide')
}

function noNull(value) {
    return value == null ? "" : value
}