const Helpers = Object.create({
    getFormInputValueByAttributeName: function (form, attributeName) {
        const element = form.querySelector(`input[name="${attributeName}"]`);
        return element.getAttribute("value");
    },
    post: function (url, data, successCallback = Helpers.success, errorCallback = Helpers.error) {
        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: successCallback,
            error: errorCallback
        });
    },
    success: function () {
        window.location.reload();
        console.log("success");
    },
    error: function (error) {
        console.error(error);
    }
});