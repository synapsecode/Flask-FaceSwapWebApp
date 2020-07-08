//declarations
main_face_display = document.getElementById("mface");
mf_upload_btn = document.getElementsByClassName("mf")[0];
second_face_display = document.getElementById("sface");
sf_upload_btn = document.getElementsByClassName("sf")[0];
output_face_display = document.getElementById("oface");
merge_btn = document.getElementById("mergebtn");
downloadbtn = document.getElementById("o_down");

API_URL = "http://localhost:5000";

//load Main Face
mf_upload_btn.onchange = (evt) => {
	console.log("Updating Main Face");
	// Display new picture
	var tgt = evt.target || window.event.srcElement,
    files = tgt.files;

	var fr = new FileReader();
	fr.onload = function () {
		main_face_display.src = fr.result;
	}
	fr.readAsDataURL(files[0]);
}

//load Second Face
sf_upload_btn.onchange = (evt) => {
	console.log("Updating Second Face");
	// Display new picture
	var tgt = evt.target || window.event.srcElement,
    files = tgt.files;

	var fr = new FileReader();
	fr.onload = function () {
		second_face_display.src = fr.result;
	}
	fr.readAsDataURL(files[0]);
}