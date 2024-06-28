function uploadButton() {
    document.getElementById('file-input').onchange = function() {
        var fileInput = document.getElementById('file-input');
        
        if ( fileInput.files.length > 1 ) {
            document.getElementById('error-message').textContent = `File count exceeds 1`;
            fileInput.value = ''; // Clear the input
        }else if ( fileInput.files[0].size > maxContentLength ) {
            document.getElementById('error-message').textContent = `File size exceeds ${maxContentLength/(1024)/1024}MB limit`;
            fileInput.value = ''; // Clear the input
        }else {
            document.getElementById('error-message').textContent = '';
            var form = document.getElementById('upload-form');
            var formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                document.getElementById('error-message').textContent = 'Error occured while uploading file';
                console.error('Error:', error);
            });
        }
    };
}

document.addEventListener('DOMContentLoaded', function() {
    uploadButton();
});