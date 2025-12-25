// File upload utilities and drag-drop functionality

// Drag and drop styling
document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    
    if (uploadArea) {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop area
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });
    }
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.backgroundColor = 'rgba(102, 126, 234, 0.05)';
    }
}

function unhighlight(e) {
    const uploadArea = document.getElementById('uploadArea');
    if (uploadArea) {
        uploadArea.style.borderColor = '';
        uploadArea.style.backgroundColor = '';
    }
}

// File validation
function validateFile(file) {
    const maxSize = 100 * 1024 * 1024; // 100MB
    const allowedTypes = [
        'application/pdf',
        'image/png',
        'image/jpeg',
        'image/jpg',
        'image/gif'
    ];
    
    if (!allowedTypes.includes(file.type)) {
        return {
            valid: false,
            error: `File type not supported: ${file.type}`
        };
    }
    
    if (file.size > maxSize) {
        return {
            valid: false,
            error: `File too large: ${file.name} (max 100MB)`
        };
    }
    
    return { valid: true };
}

// Batch file processing helper
class FileProcessor {
    constructor() {
        this.queue = [];
        this.processing = false;
        this.results = [];
    }
    
    addFiles(files) {
        files.forEach(file => {
            const validation = validateFile(file);
            if (validation.valid) {
                this.queue.push(file);
            } else {
                console.error(validation.error);
            }
        });
    }
    
    async processAll(onProgress, onComplete) {
        this.processing = true;
        this.results = [];
        
        const total = this.queue.length;
        
        for (let i = 0; i < total; i++) {
            const file = this.queue[i];
            
            if (onProgress) {
                onProgress({
                    current: i + 1,
                    total: total,
                    file: file.name,
                    percent: Math.round(((i + 1) / total) * 100)
                });
            }
            
            try {
                const result = await this.processFile(file);
                this.results.push(result);
            } catch (error) {
                this.results.push({
                    file: file.name,
                    error: error.message,
                    status: 'error'
                });
            }
        }
        
        this.processing = false;
        this.queue = [];
        
        if (onComplete) {
            onComplete(this.results);
        }
        
        return this.results;
    }
    
    async processFile(file) {
        // This is a placeholder - actual processing is done by the backend
        return {
            file: file.name,
            size: file.size,
            type: file.type,
            status: 'queued'
        };
    }
    
    clear() {
        this.queue = [];
        this.results = [];
        this.processing = false;
    }
}

// File icon helper
function getFileIconClass(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    
    const iconMap = {
        'pdf': 'fa-file-pdf',
        'png': 'fa-file-image',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'gif': 'fa-file-image'
    };
    
    return iconMap[ext] || 'fa-file';
}

// File size formatter
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Export utilities
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        FileProcessor,
        validateFile,
        getFileIconClass,
        formatBytes
    };
}
