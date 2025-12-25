// Main application logic
const API_URL = window.location.origin + '/api';

// Global state
const state = {
    selectedFiles: [],
    results: [],
    currentModal: null
};

// DOM Elements
const elements = {
    fileInput: document.getElementById('fileInput'),
    uploadArea: document.getElementById('uploadArea'),
    fileList: document.getElementById('fileList'),
    processBtn: document.getElementById('processBtn'),
    progressSection: document.getElementById('progressSection'),
    progressFill: document.getElementById('progressFill'),
    progressText: document.getElementById('progressText'),
    progressInfo: document.getElementById('progressInfo'),
    resultsSection: document.getElementById('resultsSection'),
    resultsGrid: document.getElementById('resultsGrid'),
    clearBtn: document.getElementById('clearBtn'),
    modal: document.getElementById('detailModal'),
    modalClose: document.getElementById('modalClose'),
    modalTitle: document.getElementById('modalTitle'),
    extractedText: document.getElementById('extractedText'),
    formattedJson: document.getElementById('formattedJson')
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkApiHealth();
});

// Initialize event listeners
function initializeEventListeners() {
    // File input change
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('drop', handleDrop);
    
    // Process button
    elements.processBtn.addEventListener('click', processFiles);
    
    // Clear button
    elements.clearBtn.addEventListener('click', clearResults);
    
    // Modal controls
    elements.modalClose.addEventListener('click', closeModal);
    elements.modal.addEventListener('click', (e) => {
        if (e.target === elements.modal) closeModal();
    });
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
    
    // Copy buttons
    document.getElementById('copyExtracted').addEventListener('click', () => {
        copyToClipboard(elements.extractedText.textContent, 'Extracted text');
    });
    
    document.getElementById('copyFormatted').addEventListener('click', () => {
        copyToClipboard(elements.formattedJson.textContent, 'JSON data');
    });
    
    document.getElementById('downloadJson').addEventListener('click', downloadCurrentJson);
}

// Check API health
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('API is healthy');
        }
    } catch (error) {
        console.error('API health check failed:', error);
        showNotification('Warning: Backend connection issue', 'warning');
    }
}

// Handle file selection
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

// Handle drag over
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.add('drag-over');
}

// Handle drop
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

// Add files to state
function addFiles(files) {
    const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
    
    files.forEach(file => {
        if (allowedTypes.includes(file.type)) {
            // Check if file already exists
            const exists = state.selectedFiles.some(f => 
                f.name === file.name && f.size === file.size
            );
            
            if (!exists) {
                state.selectedFiles.push(file);
            }
        } else {
            showNotification(`File type not supported: ${file.name}`, 'error');
        }
    });
    
    renderFileList();
    updateProcessButton();
}

// Render file list
function renderFileList() {
    if (state.selectedFiles.length === 0) {
        elements.fileList.innerHTML = '';
        return;
    }
    
    elements.fileList.innerHTML = state.selectedFiles.map((file, index) => `
        <div class="file-item fade-in">
            <div class="file-info">
                <i class="fas ${getFileIcon(file.type)} file-icon"></i>
                <div class="file-details">
                    <span class="file-name">${file.name}</span>
                    <span class="file-size">${formatFileSize(file.size)}</span>
                </div>
            </div>
            <button class="file-remove" onclick="removeFile(${index})">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

// Remove file from list
function removeFile(index) {
    state.selectedFiles.splice(index, 1);
    renderFileList();
    updateProcessButton();
}

// Update process button state
function updateProcessButton() {
    elements.processBtn.disabled = state.selectedFiles.length === 0;
}

// Get file icon based on type
function getFileIcon(type) {
    if (type === 'application/pdf') return 'fa-file-pdf';
    if (type.startsWith('image/')) return 'fa-file-image';
    return 'fa-file';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Process files
async function processFiles() {
    if (state.selectedFiles.length === 0) return;
    
    // Show progress section
    elements.progressSection.style.display = 'block';
    elements.processBtn.disabled = true;
    
    // Prepare form data
    const formData = new FormData();
    state.selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        updateProgress(10, 'Uploading files...');
        
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        updateProgress(50, 'Processing with AI...');
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const data = await response.json();
        
        updateProgress(90, 'Finalizing results...');
        
        // Store results
        state.results = data.results;
        
        updateProgress(100, 'Complete!');
        
        // Show results after a short delay
        setTimeout(() => {
            elements.progressSection.style.display = 'none';
            displayResults();
            clearFileSelection();
            showNotification(`Successfully processed ${data.processed} of ${data.total_files} files`, 'success');
        }, 500);
        
    } catch (error) {
        console.error('Processing error:', error);
        elements.progressSection.style.display = 'none';
        elements.processBtn.disabled = false;
        showNotification('Error processing files. Please try again.', 'error');
    }
}

// Update progress bar
function updateProgress(percent, message) {
    elements.progressFill.style.width = percent + '%';
    elements.progressText.textContent = percent + '%';
    elements.progressInfo.textContent = message;
}

// Display results
function displayResults() {
    if (state.results.length === 0) return;
    
    elements.resultsSection.style.display = 'block';
    
    elements.resultsGrid.innerHTML = state.results.map((result, index) => {
        const isSuccess = result.status === 'success';
        const previewText = isSuccess ? 
            (result.extracted_text || '').substring(0, 200) + '...' : 
            result.error;
        
        return `
            <div class="result-card ${isSuccess ? 'success' : 'error'} fade-in">
                <div class="result-header">
                    <i class="fas ${isSuccess ? 'fa-check-circle' : 'fa-exclamation-circle'} result-icon ${isSuccess ? 'success' : 'error'}"></i>
                    <div class="result-info">
                        <h4>${result.filename}</h4>
                        <span class="result-status ${isSuccess ? 'success' : 'error'}">
                            ${isSuccess ? 'Success' : 'Failed'}
                        </span>
                    </div>
                </div>
                
                <div class="result-preview">
                    <pre>${previewText}</pre>
                </div>
                
                ${isSuccess ? `
                    <div class="result-actions">
                        <button class="btn-view" onclick="viewDetails(${index})">
                            <i class="fas fa-eye"></i>
                            View Details
                        </button>
                        <button class="btn-download" onclick="downloadResult(${index})">
                            <i class="fas fa-download"></i>
                            Download
                        </button>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

// View result details in modal
function viewDetails(index) {
    const result = state.results[index];
    state.currentModal = result;
    
    elements.modalTitle.textContent = result.filename;
    elements.extractedText.textContent = result.extracted_text || 'No text extracted';
    elements.formattedJson.textContent = JSON.stringify(result.formatted_data, null, 2);
    
    elements.modal.classList.add('active');
}

// Close modal
function closeModal() {
    elements.modal.classList.remove('active');
    state.currentModal = null;
}

// Switch modal tabs
function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}Tab`).classList.add('active');
}

// Copy to clipboard
async function copyToClipboard(text, label) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification(`${label} copied to clipboard!`, 'success');
    } catch (error) {
        console.error('Copy failed:', error);
        showNotification('Failed to copy to clipboard', 'error');
    }
}

// Download result as JSON
function downloadResult(index) {
    const result = state.results[index];
    const dataStr = JSON.stringify(result.formatted_data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = result.output_file || `${result.filename}_output.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showNotification('File downloaded!', 'success');
}

// Download current modal JSON
function downloadCurrentJson() {
    if (!state.currentModal) return;
    
    const result = state.currentModal;
    const dataStr = JSON.stringify(result.formatted_data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = result.output_file || `${result.filename}_output.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showNotification('File downloaded!', 'success');
}

// Clear all results
function clearResults() {
    if (confirm('Are you sure you want to clear all results?')) {
        state.results = [];
        elements.resultsSection.style.display = 'none';
        elements.resultsGrid.innerHTML = '';
        showNotification('Results cleared', 'success');
    }
}

// Clear file selection
function clearFileSelection() {
    state.selectedFiles = [];
    elements.fileInput.value = '';
    renderFileList();
    updateProcessButton();
}

// Show notification (simple alert for now, can be enhanced)
function showNotification(message, type = 'info') {
    // Simple console log for now
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // You can implement a toast notification system here
    // For now, using alert for errors
    if (type === 'error') {
        alert(message);
    }
}

// Make functions globally accessible
window.removeFile = removeFile;
window.viewDetails = viewDetails;
window.downloadResult = downloadResult;
