// https://diw112.github.io/semanticUiAlert/
$.uiAlert = function(options) {
    var setUI = $.extend({
      textHead: 'Your user registration was successful.',
      text: 'You may now log-in with the username you have chosen',
      textcolor: '#19c3aa',
      bgcolors: '#fff',
      position: 'top-right',
      icon: '',
      time: 5,
      permanent: false
    }, options);
  
      var ui_alert = 'ui-alert-content';
        ui_alert += '-' + setUI.position;
        setUI.bgcolors ='style="background-color: '+setUI.bgcolor+';   box-shadow: 0 0 0 1px rgba(255,255,255,.5) inset,0 0 0 0 transparent;"';
        if(setUI.bgcolors === '') setUI.bgcolors ='style="background-color: ; box-shadow: 0 0 0 1px rgba(255,255,255,.5) inset,0 0 0 0 transparent;"';
      if(!$('body > .' + ui_alert).length) {
        $('body').append('<div class="ui-alert-content ' + ui_alert + '" style="width: inherit;"></div>');
      }
      var message = $('<div id="messages" class="ui icon message" ' + setUI.bgcolors + '><i class="'+setUI.icon+' icon" style="color: '+setUI.textcolor+';"></i><i class="close icon" style="color: '+setUI.textcolor+';" id="messageclose"></i><div style="color: '+setUI.textcolor+'; margin-right: 10px;">   <div class="header">'+setUI.textHead+'</div>  <p> '+setUI.text+'</p></div>  </div>');
      $('.' + ui_alert).prepend(message);
      message.animate({
        opacity: '1',
      }, 300);
      if(setUI.permanent === false){
        var timer = 0;
        $(message).mouseenter(function(){
          clearTimeout(timer);
        }).mouseleave(function(){
          uiAlertHide();
        });
        uiAlertHide();
      }
      function uiAlertHide(){
        timer = setTimeout(function() {
          message.animate({
            opacity: '0',
          }, 300, function() {
            message.remove();
          });
        }, (setUI.time * 1000) );
      }
  
      $('#messageclose')
      .on('click', function() {
        $(this)
          .closest('#messages')
          .transition('fade')
        ;
      })
    ;
  
};

$('#add_email').submit(function(e){
    e.preventDefault();
    $.ajax({
        url: '/zoro/v1/emails/add/?email=' + $('#add_email_email').val(),
        type: 'post',
        data:$('#add_email').serialize(),
        success:function() {
            $.uiAlert({
                textHead: 'Success',
                text: $('#add_email_email').val() + " can now register an account.",
                bgcolor: '#19c3aa',
                textcolor: '#fff',
                position: 'top-right',
                icon: 'checkmark box',
                time: 1
            });
            $('#add_email_email').val('');
        },
        error:function(request, status, error) {
            if (request.status == 400) {
                $.uiAlert({
                    textHead: 'Error',
                    text: "Email already exists.",
                    bgcolor: '#F2711C',
                    textcolor: '#fff',
                    position: 'top-right',
                    icon: 'warning sign',
                    time: 1
                });
            }
            else {
                $.uiAlert({
                    textHead: 'Error',
                    text: "Something went wrong.",
                    bgcolor: '#ff0000',
                    textcolor: '#fff',
                    position: 'top-right',
                    icon: 'warning sign',
                    time: 1
                });
            }
        }
    });
});

$('.ui.selection.dropdown')
  .dropdown({
    clearable: true,
    onChange: function(value, text, $selectedItem) {
        let admin = $selectedItem.find('span').text();
        if (admin == 'true') {
          $("#is_administrator").prop("checked", true);
        } else {
          $("#is_user").prop("checked", true);
        }
      }
  })
;

get_emails();
function get_emails() {
    $.ajax({
        url: '/zoro/v1/users/',
        type: 'get',
        success:function(data) {
            var users = data.users;
            console.log(users);
            $('#user_emails').empty();
            for (var i = 0; i < users.length; i++) {
                $('#user_emails').append('<div class="item" data-value="' + users[i]['email'] + '">' + users[i]['email'] + '<span style="display:none;">' + users[i]['is_administrator'] + '</span></div>');
            }
            $('.ui.selection.dropdown').dropdown('refresh');
        }
    });
}