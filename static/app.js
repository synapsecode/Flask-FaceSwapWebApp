//declarations
main_face_display = document.getElementById("mface");
mf_upload_btn = document.getElementsByClassName("mf")[0];
second_face_display = document.getElementById("sface");
sf_upload_btn = document.getElementsByClassName("sf")[0];
output_face_display = document.getElementById("oface");
merge_btn = document.getElementById("mergebtn");
downloadbtn = document.getElementById("o_down");

updateFace = (evt, disp) => {
	var tgt = evt.target,
    files = tgt.files;
	var fr = new FileReader();
	fr.onload = () => {disp.src = fr.result};
	fr.readAsDataURL(files[0]);
}

//load Main Face
mf_upload_btn.onchange = (evt) => {
	console.log("Updating Main Face");
	updateFace(evt, main_face_display)
}

//load Second Face
sf_upload_btn.onchange = (evt) => {
	console.log("Updating Second Face");
	updateFace(evt, second_face_display)
}