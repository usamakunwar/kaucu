function authCallBack(){setFiles()}function saveSignInClose(){new ButtonActive("save").start(),null!=firebase.auth().currentUser?saveAndClose():(authCallBackTask=saveAndClose,firebase.auth().signInAnonymously().catch(function(e){null!=e&&(new ButtonActive("save").stop(),alert(e))}))}function setData(e){e.status!=Status.Complete&&e.status!=Status.Incomplete&&(readOnly=!0),setReadOnly(),null!=e.files&&(files=e.files),setFiles();var t=null;null!=e.mahram&&(t=e.mahram.firstName+" "+e.mahram.lastName),checkMahram(t)}function setFiles(){Object.values(DocumentType).forEach(function(e){var t=!1;if(e==DocumentType.Permit&&changeSizeFiles(t=!needsPermit()),0!=files.length){var a=files.filter(function(t){return t.documentType==e});a.length>0?fileURL(passengerId,a[0],function(a){e==DocumentType.Visa?$("#status").html('<a class="text-white" target="_blank" href="'+a+'">Download Visa</a>'):new FileActive(e).set(a,t,readOnly)}):new FileActive(e).set(null,t,readOnly)}else new FileActive(e).set(null,t,readOnly)})}function changeSizeFiles(e){e?($("#files .col-md-4").addClass("col-md-6"),$("#files .col-md-4").removeClass("col-md-4")):($("#files .col-md-6").addClass("col-md-4"),$("#files .col-md-6").removeClass("col-md-6"))}function deleteFile(e){var t=files.map(function(e){return e.documentType}).indexOf(e);storage.ref(firebase.auth().currentUser.uid);fileStorageRef(passengerId,files[t]).delete().then(function(){files=removeFromArray(t,files),save(function(){setFiles()})}).catch(function(e){showAlert("Error","Could not delete file "+JSON.stringify(e),!0)})}function setReadOnly(){$("input, select").attr("readonly",readOnly),$("input, select").prop("disabled",readOnly),$("#dialogDelete").prop("disabled",readOnly),$("#save").prop("disabled",readOnly)}function fileUploadCallBack(e){e.documentType==DocumentType.Passport?scanPassport(e,function(t){if(setReadOnly(),new ButtonActive("save").enable(),null!=t){if(null!=t.dateOfBirth&&(t.dateOfBirth=new Date(t.dateOfBirth)),null!=t.passportExpiry){var a=new Date(t.passportExpiry);a<minPassportExpiry?showAlert("Passport expired","The minimum validity of a passport for visa has to be 6 months",!0):t.passportExpiry=a}t.status=Status.Incomplete,files.push(e),setData(t),save()}else files.push(e),loadFile(e),save(),showAlert("Passport scan failed","Please enter details manually or retry with a different image",!0);checkValid()}):(files.push(e),loadFile(e),save(),checkValid())}function loadFile(e){fileURL(passengerId,e,function(t){new FileActive(e.documentType).set(t,!1,!1)})}function scanPassport(e,t){new FileActive(e.documentType).scanning(Activity.Scanning);var a=fileStoragePath(passengerId,e);$.ajax({url:"/vision",type:"POST",data:{filePath:a},success:function(e){t(e)},error:function(e){t(null)}})}function isValid(){if(null==get("firstName"))return!1;if(null==get("lastName"))return!1;if(null==getDateValue("dateOfBirth"))return!1;if(null==get("nationality"))return!1;if(null==get("gender"))return!1;if(null==get("passportNumber"))return!1;if(null==getDateValue("passportExpiry"))return!1;if(null==getDateValue("departureDate"))return!1;if(null==getDateValue("returnDate"))return!1;if(needsPermit()){if(files.length<3)return!1}else if(files.length<2)return!1;var e=isMahramNeeded();return(!e.relation||null!=get("relationship"))&&(!e.mahram||null!=getSelectedData("mahram"))}function checkValid(){var e=isValid(),t=$("#status");t.empty(),e?(t.text(Status.Complete),t.css("background-color","#"+statusColor(Status.Complete))):(t.text(Status.Incomplete),t.css("background-color","#"+statusColor(Status.Incomplete)))}function needsPermit(){var e=get("nationality");return"United Kingdom"!=e&&null!=e}function isMahramNeeded(){var e=needsRelationship(),t=!1;return e?"Women Group"!=get("relationship")&&(t=!0):t=!1,{relation:e,mahram:t}}function needsRelationship(){var e=getDateValue("dateOfBirth");return null!=e&&getAge(e)<=17||get("gender")==Gender.Female}function checkMahram(e){var t=isMahramNeeded(),a=$("#nrelation"),n=$("#nmahram");t.relation?a.removeClass("hide"):a.addClass("hide"),t.mahram?(null==mahrams&&getMahrams(mahramCallback,e),n.removeClass("hide")):n.addClass("hide")}function getMahrams(e,t){db.collection("Client").doc(firebase.auth().currentUser.uid).collection("Passenger").where("gender","==",Gender.Male).get().then(function(a){var n=[];a.forEach(function(e){const t=e.data();var a=t.dateOfBirth;if(null!=a&&getAge(a.toDate())>17){var i={};i.firstName=t.firstName,i.lastName=t.lastName,i.passportNumber=t.passportNumber,i.id=e.id,n.push(i)}}),e(n,t)}).catch(function(e){})}function mahramCallback(e,t){mahrams=e,$("#mahram").empty(),$("#mahram").append("<option disabled selected value>Select</option>"),mahrams.forEach(function(e,t){var a=JSON.stringify(e);$("#mahram").append("<option data-value="+a+">"+e.firstName+" "+e.lastName+"</option>")}),null!=t&&$("#mahram").val(t)}$("input,select").change(function(){checkValid()}),$("#gender,#nationality,#relationship,#dateOfBirth").change(function(){checkMahram(null)}),$("#dateOfBirth").on("changeDate",function(e){checkMahram(null)}),$("#nationality").change(function(){countries.includes(this.value)||(this.value=null)});var minDOB=new Date;$("#dateOfBirth").datepicker({format:"dd/mm/yyyy",keyboardNavigation:!1,forceParse:!0,autoclose:!0,endDate:minDOB,startView:"years"}).on("changeDate",function(e){checkValid()}),$("#dateOfBirth").datepicker("setEndDate",minDOB);var minPassportExpiry=minPassportExpiryDate();$("#passportExpiry").datepicker({format:"dd/mm/yyyy",keyboardNavigation:!1,forceParse:!0,autoclose:!0,startView:"years",startDate:minPassportExpiry}).on("changeDate",function(e){checkValid()}),$("#departureDate, #returnDate").datepicker({format:"dd/mm/yyyy",keyboardNavigation:!1,forceParse:!0,autoclose:!0,startDate:config.minDepartureDate}).on("changeDate",function(e){checkValid()}),$("#nationality").typeahead({source:countries,afterSelect:function(e){setFiles()}}),$("#relationship").append("<option disabled selected value>Select</option>"),Object.values(Relationship).forEach(function(e){$("#relationship").append('<option value="'+e+'">'+e+"</option>")}),$("#gender").append("<option disabled selected value>Select</option>"),Object.values(Gender).forEach(function(e){$("#gender").append('<option value="'+e+'">'+e+"</option>")});