$(document).ready(function () {
    $("#question-form").submit(function (event) {
        event.preventDefault();
        let data = new FormData(this);
        let form = this;
        let thinking_spinner = $("#thinking-spinner");
        let message_placeholder = $("#message-placeholder");

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

            axios({
                method: "post",
                url: "/answer",
                data: data,
                headers: {"Content-Type": "multipart/form-data"}
            }).then(function (response) {
                //handle success
                message_placeholder.before(response.data);
                form.reset();

                thinking_spinner.css("display", "none")

            }).catch(function (response) {
                //handle error
                console.log(response);
            });

        }).catch(function (response) {
            //handle error
            console.log(response);
        });
    });
});