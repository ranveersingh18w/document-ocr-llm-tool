document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const outputContainer = document.getElementById('outputContainer');

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const files = fileInput.files;

        if (files.length === 0) {
            alert('Please select at least one file to upload.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await fetch('/upload', {
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
            const fileDiv = document.createElement('div');
            fileDiv.classList.add('output-file');
            fileDiv.innerHTML = `
                <h3>${file.name}</h3>
                <a href="${file.outputUrl}" target="_blank">View Output</a>
            `;
            outputContainer.appendChild(fileDiv);
        });
    }
});