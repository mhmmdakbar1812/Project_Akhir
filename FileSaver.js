function take_snapshot() {
  Webcam.snap(function(data_uri) {
    // Menampilkan hasil snapshot di halaman web
    var results = document.getElementById('results');
    results.innerHTML = '<img src="' + data_uri + '"/>';

    // Mengubah data URI menjadi blob agar bisa diunduh sebagai file
    var blob = dataURItoBlob(data_uri);

    // Mengunduh file dengan menggunakan library FileSaver.js
    saveAs(blob, 'snapshot.jpg');
  });
}

// Mengubah data URI menjadi blob agar bisa diunduh sebagai file
function dataURItoBlob(dataURI) {
  var byteString = atob(dataURI.split(',')[1]);
  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], { type: 'image/jpeg' });
}
