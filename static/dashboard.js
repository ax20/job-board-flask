$(document).ready(function () {
    $("#password").hide().prop('required', false);
    $("#purge_button").hide(); 

    $("#purge_button").click(function () {
        $('#manage_posts').attr('action', '/new/' + $('#password').val() + '/');
        $('#manage_posts').submit();
    });

    $('#modes').change(function () {
        $("#password").hide().prop('required', false);
        $("#purge_button").hide().prop('required', false);
        $("#id").show().prop('required', true);
        $("#url").show().prop('required', true);
        $("#title").show().prop('required', true);
        $("#position").show().prop('required', true);
        $("#company").show().prop('required', true);
        $("#summary").show().prop('required', true);
        $("#description").show().prop('required', true);
        $("#location").show().prop('required', true);
        $("#expires_on").show().prop('required', true);
        $("#posted_on").show().prop('required', true);
        $("submit_button").show();

        if (this.value == 0) {
            $("#posted_on").hide().prop('required', false);
            $("#id").hide().prop('required', false);
            $('#manage_posts').attr('action', '/new/');
        } else if (this.value == 1) {
            $('#manage_posts').attr('action', '/edit/');
        } else if (this.value == 2) {
            $('#manage_posts').attr('action', '/delete/');
            $("#posted_on").hide().prop('required', false);
            $("#url").hide().prop('required', false);
            $("#title").hide().prop('required', false);
            $("#position").hide().prop('required', false);
            $("#company").hide().prop('required', false);
            $("#summary").hide().prop('required', false);
            $("#description").hide().prop('required', false);
            $("#location").hide().prop('required', false);
            $("#expires_on").hide().prop('required', false);
        } else if (this.value == 3) {
            $("#id").hide().prop('required', false);
            $("#posted_on").hide().prop('required', false);
            $("#url").hide().prop('required', false);
            $("#title").hide().prop('required', false);
            $("#position").hide().prop('required', false);
            $("#company").hide().prop('required', false);
            $("#summary").hide().prop('required', false);
            $("#description").hide().prop('required', false);
            $("#location").hide().prop('required', false);
            $("#expires_on").hide().prop('required', false);
            $("#submit_button").hide();
            $("#password").show().prop('required', true);
            $("#purge_button").show();
        }
    });
});