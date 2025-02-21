document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('file-input');
    const formData = new FormData();
    for (const file of fileInput.files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch('http://127.0.0.1:8080/predict', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            let resultText = '';
            result.forEach((res, index) => {
                resultText += `Image ${index + 1}: Predicted Race: ${res.predicted_race}\n`;
            });
            document.getElementById('result').innerText = resultText;
        } else {
            const errorData = await response.json();
            document.getElementById('result').innerText = `Error: ${errorData.error || 'Unable to get prediction'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error: Unable to get prediction';
    }
});

document.querySelector('.custom-file-upload').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function() {
    const fileList = Array.from(this.files).map(file => file.name).join(', ');
    document.querySelector('.custom-file-upload').innerText = fileList || 'Choose a file...';
});