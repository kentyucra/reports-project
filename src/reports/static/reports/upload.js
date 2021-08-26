const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')

Dropzone.autoDiscover = false

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

const myDropzone = new Dropzone('#my-dropzone', {
    url: '/reports/upload/',
    init: function() {
        this.on('sending', function(file, xhr, formData) {
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })

        this.on('success', function(file, response) {
            const ex = response.ex
            if (ex) {
                alertBox.innerHTML = handleAlerts('danger', 'The csv file ALREADY was uploaded!!')
            } else {
                alertBox.innerHTML = handleAlerts('success', 'Your file has been uploaded SUCCESSFULLY!!')
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv'
})