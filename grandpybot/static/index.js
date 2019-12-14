$(document).ready(function () {
    $("#question-form").submit(function (event) {
        event.preventDefault();
        let data = new FormData(this);
        let form = this;
        let thinking_spinner = $("#thinking-spinner");
        let message_placeholder = $("#message-placeholder");
        let messages_box = $('#messages-box');

        axios({
            method: "post",
            url: "/",
            data: data,
            headers: {"Content-Type": "multipart/form-data"}
        }).then(function (response) {
            //handle success
            message_placeholder.before(response.data);
            form.reset();
            thinking_spinner.css("display", "");
            messages_box.animate({scrollTop: 99999}, 'slow');

            axios({
                method: "post",
                url: "/answer",
                data: data,
                headers: {"Content-Type": "multipart/form-data"}
            }).then(function (response) {
                //handle success
                message_placeholder.before(response.data);
                thinking_spinner.css("display", "none");
                messages_box.animate({scrollTop: 10000}, 'slow');
            }).catch(function (error) {
                thinking_spinner.css("display", "none");

                new Noty({
                    theme: "bootstrap-v4",
                    text: error.response.data,
                    type: "error",
                    timeout: 3000
                }).show();
            });

        }).catch(function (error) {
            thinking_spinner.css("display", "none");

            new Noty({
                theme: "bootstrap-v4",
                text: error.response.data,
                type: "error",
                timeout: 3000
            }).show();
        });
    });
});