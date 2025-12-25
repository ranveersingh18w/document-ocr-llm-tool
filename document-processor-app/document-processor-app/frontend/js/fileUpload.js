document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const uploadButton = document.getElementById('upload-button');
    const outputContainer = document.getElementById('output-container');

    uploadButton.addEventListener('click', async () => {
        const files = fileInput.files;
        if (files.length === 0) {
            alert('Please select files to upload.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('File upload failed.');
            }

            const result = await response.json();
            displayOutput(result);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while uploading files.');
        }
    });

    function displayOutput(result) {
        outputContainer.innerHTML = '';
        result.forEach(file => {
            const fileLink = document.createElement('a');
            fileLink.href = file.outputUrl;
            fileLink.textContent = file.fileName;
            fileLink.target = '_blank';
            outputContainer.appendChild(fileLink);
            outputContainer.appendChild(document.createElement('br'));
        });
    }
});