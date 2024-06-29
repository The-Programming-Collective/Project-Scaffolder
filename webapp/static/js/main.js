function uploadButton() {
    document.getElementById('file-input').onchange = function() {
        var fileInput = document.getElementById('file-input');
        
        if ( fileInput.files.length > 1 ) {
            document.getElementById('error-message').textContent = `File count exceeds 1`;
            fileInput.value = '';
        }else if ( fileInput.files[0].size > maxContentLength ) {
            document.getElementById('error-message').textContent = `File size exceeds ${maxContentLength/(1024)/1024}MB limit`;
            fileInput.value = '';
        }else {
            document.getElementById('error-message').textContent = '';
            var form = document.getElementById('upload-form');
            var formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                var status = response.status;
                return response.json().then(data => {
                    return { status: status, data: data };
                });
            })
            .then(result => {
                if(!result.ok) {
                    document.getElementById('error-message').textContent = `${result.data.error}`;
                }
            })
            .catch(error => {
                document.getElementById('error-message').textContent = 'Error occured while uploading file';
            });
        }
        setTimeout(function() {
            document.getElementById('error-message').textContent = '';
        }, 5000);
    };
}

document.addEventListener('DOMContentLoaded', function() {
    uploadButton();
});
