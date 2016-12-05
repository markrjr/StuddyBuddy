function uploadFile()
{
  console.log("This was run.")
  var files = document.getElementById("files-dialog");
  var upload = document.getElementById('upload-dialog');
  var upload_btn = document.getElementById('upload-btn');

  if(upload.style.display === "none")
  {
      files.style.display = "none";
      upload.style.display = "block";
      upload_btn.innerText = "Cancel";
  }
  else if(upload.style.display === "block")
  {
      upload.style.display = "none";
      files.style.display = "block";
      upload_btn.innerText = "Upload";
  }

}